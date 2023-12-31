#  Copyright (c) 2023. Philip Alexander-Lees
#
#  All rights reserved.
#
#  MIT License
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the “Software”), to deal
#  in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the Software
#  is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
#  OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
"""AbilityScore Family Classes

"""
from typing import Any, List, Union

import pandas as pd

from dnd5eapy.core import DnD5eAPIObj
from dnd5eapy.skills import Skills

DEFAULT_FULL_NAME_COLUMN_NAME: str = "full_name"
DEFAULT_DESC_COLUMN_NAME: str = "desc"
DEFAULT_SKILLS_COLUMN_NAME: str = "skills"


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
    """Child class of AbilityScores for handling a given ability score
    out of the ability-scores api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target an ability score.
    kwargs: optional
        Keyword arguments to pass to `super().__init__()`

    """
    url_leaf: str = "/api/ability-scores/*"

    def __init__(
            self,
            url_leaf: str = url_leaf.replace("/*", "/cha"),
            full_name_column_name: str = DEFAULT_FULL_NAME_COLUMN_NAME,
            desc_column_name: str = DEFAULT_DESC_COLUMN_NAME,
            skills_column_name: str = DEFAULT_SKILLS_COLUMN_NAME,
            **kwargs):
        """Constructs the `AbilityScore` instance.
        """
        self._full_name_column_name = full_name_column_name
        self._desc_column_name = desc_column_name
        self._skills_column_name = skills_column_name
        super().__init__(url_leaf, **kwargs)

    @property
    def full_name_column_name(self) -> str:
        """self._full_name_column_name

        Returns
        -------
        str
        """
        return self._full_name_column_name

    @full_name_column_name.setter
    def full_name_column_name(self, name: Union[str, int]):
        if self.full_name_column_name in self.columns:
            self.df = self.df.rename(columns={self.full_name_column: name})
        self._full_name_column_name = name

    @property
    def full_name_column(self) -> pd.Series:
        """self[self.full_name_column_name]

        Returns
        -------
        pandas.Series
        """
        try:
            return self[self.full_name_column_name]
        except KeyError as kerr:
            raise KeyError(self.full_name_column_name) from kerr

    @full_name_column.setter
    def full_name_column(self, data: pd.Series):
        self[self.full_name_column_name] = data
        self.full_name_column_name = data.name

    @property
    def full_name(self) -> Union[str, Any]:
        """self.df["full_name"].iat[0]

        Returns
        -------
        Union[str, Any]
        """
        return self.full_name_column.iat[0]

    @full_name.setter
    def full_name(self, value: Any):
        self.full_name_column.iat[0] = value

    @property
    def desc_column_name(self) -> str:
        """self._desc_column_name
        Returns
        -------
        str
        """
        return self._desc_column_name

    @desc_column_name.setter
    def desc_column_name(self, name: Union[str, int]):
        if self.desc_column_name in self.columns:
            self.df = self.df.rename(columns={self.desc_column_name: name})
        self._desc_column_name = name

    @property
    def desc_column(self) -> pd.Series:
        """self.df[self.desc_column_name]

        Returns
        -------
        pandas.Series
        """
        try:
            return self[self.desc_column_name]
        except KeyError as kerr:
            raise KeyError(self.desc_column_name) from kerr

    @desc_column.setter
    def desc_column(self, data: pd.Series):
        self[self.desc_column_name] = data
        self.desc_column_name = data.name

    @property
    def desc(self) -> List[str]:
        """self.desc_column.iat[0]

        Returns
        -------
        List[str]
        """
        return self.desc_column.iat[0]

    @desc.setter
    def desc(self, value: Any):
        self.desc_column.iat[0] = value

    @property
    def skills_column_name(self) -> str:
        """self._skills_column_name

        Returns
        -------
        str
        """
        return self._skills_column_name

    @skills_column_name.setter
    def skills_column_name(self, name: Union[str, int]):
        if self.skills_column_name in self.columns:
            self.df = self.df.rename(columns={self.skills_column_name: name})
        self._skills_column_name = name

    @property
    def skills_column(self) -> pd.Series:
        """self[self.skills_column_name]

        Returns
        -------
        pandas.Series
        """
        return self[self.skills_column_name]

    @skills_column.setter
    def skills_column(self, data: pd.Series):
        self[self.skills_column_name] = data
        self.skills_column_name = data.name

    @property
    def skills_df(self) -> pd.DataFrame:
        """self.df["skills"].iat[0]

        Returns
        -------
        pandas.DataFrame
        """
        return self.skills_column.iat[0]

    @skills_df.setter
    def skills_df(self, dframe: pd.DataFrame):
        self.skills_column.iat[0] = dframe

    @property
    def skills(self) -> Skills:
        """skills.Skills(data=self.skills_df)

        Returns
        -------
        skills.Skills
        """
        return Skills(
            url_leaf=self.url_leaf,
            url_root=self.url_root,
            headers=self.requests_args.get("headers"),
            timeout=self.requests_args.get("timeout"),
            data=self.skills_df,
            name_column_name=self.name_column_name,
            url_column_name=self.url_column_name,
            obj_column_name=self.obj_column_name,
            index_name=self._index_name,
        )

    @skills.setter
    def skills(self, skills_obj: Skills):
        self.skills_column.iat[0] = skills_obj.df

    @property
    def name(self) -> str:
        """self.name_column.iat[0]

        Returns
        -------
        str
        """
        return self.name_column.iat[0]

    @name.setter
    def name(self, name: str):
        self.name_column.iat[0] = name

    @property
    def url(self) -> str:
        """self.url_column.iat[0]

        Returns
        -------
        str
        """
        return self.url_column.iat[0]

    @url.setter
    def url(self, url: str):
        self.url_column.iat[0] = url
