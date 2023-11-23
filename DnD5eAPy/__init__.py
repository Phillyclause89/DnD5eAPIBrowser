#  Copyright (c) 2023. Philip Alexander-Lees
#
#  All rights reserved.
#
#  MIT License
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies
#  or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
#  THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#
#  All rights reserved.
#
#  MIT License
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#
import warnings
from typing import Any, Dict

import pandas as pd
import requests


class DnD5eAPIObj:
    """Base parent class for most DnD5eAPy classes.

    Parameters
    ----------
    url_leaf : str, optional
        Sets the `url_leaf` attribute of the `DnD5eAPIObj` instance.
    url_root : str, optional
        Sets the `url_root` attribute of the `DnD5eAPIObj` instance.
    headers : Dict[str, str], optional
        Sets the `headers` attribute of the `DnD5eAPIObj` instance.

    Attributes
    ----------
    df: pandas.DataFrame
        DataFrame representation of the `json` object returned by `DnD5eAPIObj.__get_df__()`.
    json: Dict[str, object]
        The decoded json dictionary returned by `DnD5eAPIObj.__get_json__()`.
    response: requests.Response
        The `response` object returned by `DnD5eAPIObj.__get_response__()`.
    url: str
        The full url string used to fetch the `response` (i.e. f"{url_root}{url_leaf}").
    url_root: str
        The api server root of the `url`.
    url_leaf: str
        The api function path of the `url`.
    headers: Dict[str, str]
        The headers used in the api request.

    """
    leaf_constructors: Dict[str, Any]
    url_root: str = "https://www.dnd5eapi.co"
    url_leaf: str = "/api"
    url: str = f"{url_root}{url_leaf}"
    headers: Dict[str, str] = {'Accept': 'application/json'}
    df: pd.DataFrame = pd.DataFrame()
    response: requests.Response = requests.Response()
    json: Dict[str, object] = {}

    def __init__(self, url_leaf: str = url_leaf, url_root: str = url_root,
                 headers: Dict[str, str] = None):
        """Constructs the `DnD5eAPIObj` instance


        """
        if headers is None:
            headers = {'Accept': 'application/json'}
        self.headers = headers
        self.url_leaf = url_leaf
        self.url_root = url_root
        self.url = f"{self.url_root}{self.url_leaf}"
        self.leaf_constructors = get_leaf_constructor_map()
        self.response = self.__get_response__()
        self.json = self.__get_json__()
        self.df = self.__get_df__()

    def refresh(self):
        """Updates the `DnD5eAPIObj` instance with a new api request.
            The results of the update are dependent on the instance's current `url` and `header` property values.


        """
        self.response = self.__get_response__()
        self.json = self.__get_json__()
        self.df = self.__get_df__()

    def create_instances_from_urls(self):
        """Attempts to update api urls in the `df` with initialized `DnD5eAPIObj` objects.

        Returns
        -------
        None

        """

        try:
            self.df["obj"] = self.df["url"].apply(
                lambda url_leaf: self.leaf_constructors.get(
                    url_leaf, self.leaf_constructors.get(
                        "/".join(url_leaf.split("/")[:-1]) + "/*"))(url_leaf))
        except KeyError as e:
            if e.args[0] == "url":
                return warnings.warn(
                    f"INVALID RESPONSE STATUS CODE\nThe DataFrame does not contain a 'url' column:\n{self.df.columns}",
                    ResourceWarning, stacklevel=2
                )
            raise e

    def __get_response__(self) -> requests.Response:
        """Gets the api request response via `requests`.
            This method is called at initialization and when the `refresh` method is called.

            Results of `__get_response__` method calls are dependent on the `url` and `headers` attributes.

        Returns
        -------
        requests.Response


        """
        return requests.get(self.url, headers=self.headers)

    def __get_json__(self) -> Dict[str, object]:
        """Gets the json decoded content of `response`.
            This method is called at initialization and when the `refresh` method is called.

            If `response.status_code` does not equal `200` then `{"status_code": response.status_code}` is returned.

            Results of `__get_json__` method calls are dependent on the `response` attribute.

        Returns
        -------
        Dict[str, object]
            json decoded content of `response.json()` or `{"status_code": response.status_code}`.

        """
        status_code = self.response.status_code
        if status_code == 200:
            return self.response.json()
        return {"status_code": status_code}

    def __eq__(self, other):
        return self.df.__eq__(other)

    def __bool__(self):
        if self.df.columns[0] == "status_code":
            return False
        return self.df.__bool__()

    def __str__(self) -> str:
        """Returns `str(json)`.

        Returns
        -------
        str

        """
        return self.__repr__().replace(" at ", f" from {self.response.url} at ")

    def __get_df__(self) -> pd.DataFrame:
        """gets the `df` from `self.json`.
            If the keys `'count'` and `'results'` are in `json.keys()` then the initial DataFrame will be
            `df = pd.DataFrame(json.get('results'))`, otherwise `df = pd.DataFrame([self.json])` will be initialized.

            If the key `'index'` is in `df.columns` then the final DataFrame returned
            will be indexed by that key's value(s) (i.e. `return df.set_index('index')`).

            Results of `__get_df__` method calls are dependent on the `json` attribute.

        Returns
        -------
        pandas.DataFrame
            Two-dimensional, size-mutable, potentially heterogeneous tabular data representation of
            the `self.json` object sourced from the API response.

        """
        if self.json.get('count') and self.json.get('results'):
            df = pd.DataFrame(self.json.get('results'))
            return df.set_index("index") if 'index' in df.columns else df
        df = pd.DataFrame([self.json])
        if self.response.url == self.url and self.url_leaf == "/api":
            return df.transpose().rename(columns={0: "url"}).rename_axis("index")
        return df.set_index("index") if 'index' in df.columns else df

    def __getitem__(self, item):
        return self.df.__getitem__(item)

    def __len__(self):
        return self.df.__len__()

    def __setitem__(self, key, value):
        return self.df.__setitem__(key, value)

    def __contains__(self, item):
        return self.df.__contains__(item)

    def __iter__(self):
        return self.df.__iter__()

    def __next__(self):
        return self.df.__next__()

    def __add__(self, other):
        return self.df.__add__(other)

    def __sub__(self, other):
        return self.df.__sub__(other)

    def __mul__(self, other):
        return self.df.__mul__(other)

    def __truediv__(self, other):
        return self.df.__truediv__(other)

    def __pow__(self, power, modulo=None):
        return self.df.__pow__(power, modulo)


class AbilityScores(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the ability-scores api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target ability-scores api.
        
    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`
        
    
    """
    url_leaf: str = "/api/ability-scores"

    def __init__(self, url_leaf: str = url_leaf, **kwargs):
        """Constructs the `AbilityScores` instance.


        """
        super().__init__(url_leaf, **kwargs)


class AbilityScore(AbilityScores):
    """Child class of AbilityScores for handling a given ability score out of the ability-scores api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target an ability score.
    kwargs: optional
        Keyword arguments to pass to `super().__init__()`

    """
    url_leaf: str = "/api/ability-scores/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/cha"), **kwargs):
        """Constructs the `AbilityScore` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Alignments(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the alignments api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target alignments api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/alignments"

    def __init__(self, url_leaf=url_leaf, **kwargs):
        """Constructs the `Alignments` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Alignment(Alignments):
    """Child class of `Alignments` for handling an alignment out of the alignments api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target an alignment.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/alignments/*"

    def __init__(self, url_leaf=url_leaf.replace("/*", "/chaotic-evil"), **kwargs):
        """Constructs the `Alignment` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Backgrounds(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the backgrounds api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target backgrounds api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/backgrounds"

    def __init__(self, url_leaf=url_leaf, **kwargs):
        """Constructs the `Backgrounds` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Background(Backgrounds):
    """Child class of `Backgrounds` for handling a background out of the backgrounds api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a background.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/backgrounds/*"

    def __init__(self, url_leaf=url_leaf.replace("/*", "/acolyte"), **kwargs):
        """Constructs the `Background` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Classes(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the classes api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target classes api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/classes"

    def __init__(self, url_leaf=url_leaf, **kwargs):
        """Constructs the `Classes` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Class(Classes):
    """Child class of `Classes` for handling a class (oh god what did I just do with this class name!
    I really hope case sensitivity pulls its weight here!) out of the classes api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a class.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/classes/*"

    def __init__(self, url_leaf=url_leaf.replace("/*", "/barbarian"), **kwargs):
        """Constructs the `Class` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Conditions(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the conditions api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target conditions api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/conditions"

    def __init__(self, url_leaf=url_leaf, **kwargs):
        """Constructs the `Conditions` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Condition(Conditions):
    """Child class of `Conditions` for handling a condition out of the conditions api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a condition.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/conditions/*"

    def __init__(self, url_leaf=url_leaf.replace("/*", "/blinded"), **kwargs):
        """Constructs the `Condition` instance.


        """
        super().__init__(url_leaf, **kwargs)


class DamageTypes(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the damage-types api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target damage-types api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/damage-types"

    def __init__(self, url_leaf=url_leaf, **kwargs):
        """Constructs the `DamageTypes` instance.


        """
        super().__init__(url_leaf, **kwargs)


class DamageType(DamageTypes):
    """Child class of `DamageTypes` for handling a damage-type out of the damage-types api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a damage-type.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/damage-types/*"

    def __init__(self, url_leaf=url_leaf.replace("/*", "/acid"), **kwargs):
        """Constructs the `DamageType` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Equipment(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the equipment api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target equipment api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/equipment"

    def __init__(self, url_leaf=url_leaf, **kwargs):
        """Constructs the `Equipment` instance.


        """
        super().__init__(url_leaf, **kwargs)


class EquipmentItem(Equipment):
    """Child class of `Equipment` for handling an equipment item (it really bugs me that
    this is the first child class that forces me to break my naming convention of
    just trimming an 's' off the end of the parent class name.) out of the
    equipment api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target equipment api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/equipment/*"

    def __init__(self, url_leaf=url_leaf.replace("/*", "/abacus"), **kwargs):
        """Constructs the `EquipmentItem` instance.


        """
        super().__init__(url_leaf, **kwargs)


class EquipmentCategories(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the equipment-categories api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target equipment-categories api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/equipment-categories"

    def __init__(self, url_leaf=url_leaf, **kwargs):
        """Constructs the `EquipmentCategories` instance.


        """
        super().__init__(url_leaf, **kwargs)


class EquipmentCategory(EquipmentCategories):
    """Child class of `EquipmentCategories` for handling an equipment-category out of the equipment-categories api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target an equipment-category.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/equipment-categories/*"

    def __init__(self, url_leaf=url_leaf.replace("/*", "/adventuring-gear"), **kwargs):
        """Constructs the `EquipmentCategory` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Feats(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the feats api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target feats api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/feats"

    def __init__(self, url_leaf: str = url_leaf, **kwargs):
        """Constructs the `Feats` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Feat(Feats):
    """Child class of `Feats` for handling a feat out of the feats api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a feat.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/feats/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/grappler"), **kwargs):
        """Constructs the `Feat` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Features(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the features api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target features api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/features"

    def __init__(self, url_leaf: str = "/api/features", **kwargs):
        """Constructs the `Features` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Feature(Features):
    """Child class of `Features` for handling a feature out of the features api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a feature.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/features/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/action-surge-1-use"), **kwargs):
        """Constructs the `Feature` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Languages(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the languages api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target languages api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/languages"

    def __init__(self, url_leaf: str = url_leaf, **kwargs):
        """Constructs the `Languages` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Language(Languages):
    """Child class of `Languages` for handling a language out of the languages api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a language.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/languages/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/abyssal"), **kwargs):
        """Constructs the `Language` instance.


        """
        super().__init__(url_leaf, **kwargs)


class MagicItems(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the magic-items api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target magic-items api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/magic-items"

    def __init__(self, url_leaf: str = url_leaf, **kwargs):
        """Constructs the `MagicItems` instance.


        """
        super().__init__(url_leaf, **kwargs)


class MagicItem(MagicItems):
    """Child class of `MagicItems` for handling data out of the magic-items api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target magic-items api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/magic-items/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/adamantine-armor"), **kwargs):
        """Constructs the `MagicItem` instance.


        """
        super().__init__(url_leaf, **kwargs)


class MagicSchools(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the magic-schools api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target magic-schools api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/magic-schools"

    def __init__(self, url_leaf: str = url_leaf, **kwargs):
        """Constructs the `MagicSchools` instance.


        """
        super().__init__(url_leaf, **kwargs)


class MagicSchool(MagicSchools):
    """Child class of `MagicSchools` for handling a magic-school out of the magic-schools api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a magic-school.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/magic-schools/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/abjuration"), **kwargs):
        """Constructs the `MagicSchool` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Monsters(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the monsters api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target monsters api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/monsters"

    def __init__(self, url_leaf: str = url_leaf, **kwargs):
        """Constructs the `Monsters` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Monster(Monsters):
    """Child class of `Monsters` for handling a monster out of the monsters api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a monster.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/monsters/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/aboleth"), **kwargs):
        """Constructs the `Monster` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Proficiencies(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the proficiencies api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target proficiencies api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/proficiencies"

    def __init__(self, url_leaf: str = url_leaf, **kwargs):
        """Constructs the `Proficiencies` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Proficiency(Proficiencies):
    """Child class of `Proficiencies` for handling a proficiency out of the proficiencies api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target proficiency.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/proficiencies/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/alchemists-supplies"), **kwargs):
        """Constructs the `Proficiency` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Races(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the races api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target races api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/races"

    def __init__(self, url_leaf: str = url_leaf, **kwargs):
        """Constructs the `Races` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Race(Races):
    """Child class of `Races` for handling a race out of the races api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a race.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/races/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/dragonborn"), **kwargs):
        """Constructs the `Race` instance.


        """
        super().__init__(url_leaf, **kwargs)


class RuleSections(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the rule-sections api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target rule-sections api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/rule-sections"

    def __init__(self, url_leaf: str = url_leaf, **kwargs):
        """Constructs the `RuleSections` instance.


        """
        super().__init__(url_leaf, **kwargs)


class RuleSection(RuleSections):
    """Child class of `RuleSections` for handling a rule-section out of the rule-sections api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a rule-section.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/rule-sections/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/ability-checks"), **kwargs):
        """Constructs the `RuleSection` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Rules(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the rules api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target rules api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/rules"

    def __init__(self, url_leaf: str = url_leaf, **kwargs):
        """Constructs the `Rules` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Rule(Rules):
    """Child class of `Rules` for handling a rule out of the rules api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target rules api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/rules/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/adventuring"), **kwargs):
        """Constructs the `Rule` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Skills(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the skills api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target skills api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/skills"

    def __init__(self, url_leaf: str = url_leaf, **kwargs):
        """Constructs the `Skills` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Skill(Skills):
    """Child class of `Skills` for handling a skill out of the skills api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a skill.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/skills/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/acrobatics"), **kwargs):
        """Constructs the `Skill` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Spells(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the spells api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target spells api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/spells"

    def __init__(self, url_leaf: str = url_leaf, **kwargs):
        """Constructs the `Spells` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Spell(Spells):
    """Child class of `Spells` for handling a spell out of the spells api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a spell.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/spells/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/acid-arrow"), **kwargs):
        """Constructs the `Spell` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Subclasses(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the subclasses api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target subclasses api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/subclasses"

    def __init__(self, url_leaf: str = url_leaf, **kwargs):
        """Constructs the `Subclasses` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Subclass(Subclasses):
    """Child class of `Subclasses` for handling a subclass out of the subclasses api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a subclass.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/subclasses/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/berserker"), **kwargs):
        """Constructs the `Subclass` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Subraces(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the subraces api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target subraces api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/subraces"

    def __init__(self, url_leaf: str = url_leaf, **kwargs):
        """Constructs the `Subraces` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Subrace(Subraces):
    """Child class of `Subraces` for handling a subrace out of the subraces api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a subrace.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/subraces/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/high-elf"), **kwargs):
        """Constructs the `Subrace` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Traits(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the traits api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target traits api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/traits"

    def __init__(self, url_leaf: str = url_leaf, **kwargs):
        """Constructs the `Traits` instance.


        """
        super().__init__(url_leaf, **kwargs)


class Trait(Traits):
    """Child class of `Traits` for handling a trait out of the traits api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a trait.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/traits/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/artificers-lore"), **kwargs):
        """Constructs the `Trait` instance.


        """
        super().__init__(url_leaf, **kwargs)


class WeaponProperties(DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the weapon-properties api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target weapon-properties api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/weapon-properties"

    def __init__(self, url_leaf: str = url_leaf, **kwargs):
        """Constructs the `WeaponProperties` instance.


        """
        super().__init__(url_leaf, **kwargs)


class WeaponProperty(WeaponProperties):
    """Child class of `WeaponProperties` for handling a weapon-property out of the weapon-properties api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target a weapon-property.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/weapon-properties/*"

    def __init__(self, url_leaf: str = url_leaf.replace("/*", "/ammunition"), **kwargs):
        """Constructs the `WeaponProperty` instance.


        """
        super().__init__(url_leaf, **kwargs)


def get_leaf_constructor_map() -> Dict[str, Any]:
    def all_subclasses(cls):
        return set(cls.__subclasses__()).union(
            [s for c in cls.__subclasses__() for s in all_subclasses(c)])

    return {**{DnD5eAPIObj.url_leaf: DnD5eAPIObj}, **{cls.url_leaf: cls for cls in all_subclasses(DnD5eAPIObj)}}
