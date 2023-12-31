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
"""tests for dnd5eapy!

"""
from typing import Any, Dict, Type, Union
from unittest import TestCase
import pandas as pd
from numpy.typing import NDArray
from pandas import DataFrame

import dnd5eapy
import expected as exp

NEW_NAME_COLUMN_NAME = "D&D Name"
NEW_URL_COLUMN_NAME = "Uniform Resource Locator"
NEW_OBJ_COLUMN_NAME = "D&D Object"


class TestDnD5eAPIObj(TestCase):
    """test core class
    """
    bad_dnd: Union[dnd5eapy.DnD5eAPIObj, Any]
    dnd: Union[dnd5eapy.DnD5eAPIObj, Any]
    constructor: Type[dnd5eapy.DnD5eAPIObj]

    def setUp(self) -> None:
        """
        Returns
        -------
        None

        """
        self.constructor = dnd5eapy.DnD5eAPIObj
        self.dnd = self.constructor()
        self.bad_dnd = self.constructor(r"/api/Bad_Leaf_69_420")

    def test__get_json__(self) -> None:
        """

        Returns
        -------

        """
        result_json: Union[Dict[str, object], Any] = self.dnd.__get_json__
        self.assertEqual(exp.GOOD_BASE_RESPONSE, result_json)
        bad_result: Union[Dict[str, object], Any] = self.bad_dnd.__get_json__
        self.assertEqual(exp.BAD_404_RESPONSE, bad_result)

    def test__get_df__(self) -> None:
        """

        Returns
        -------

        """
        result_df: DataFrame = self.dnd.__df_from_response__
        self.assertEqual("/api/ability-scores", result_df.at["ability-scores", "url"])
        bad_result_df: DataFrame = self.bad_dnd.__df_from_response__
        self.assertEqual(404, bad_result_df.at[0, "status_code"])

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        # Good Dnd tests
        self.assertEqual(exp.URL_ROOT, self.dnd.url_root)
        self.assertEqual("/api", self.dnd.url_leaf)
        self.assertEqual(exp.HEADERS, self.dnd.requests_args["headers"])
        self.assertIsInstance(self.dnd.df, pd.DataFrame)
        # Bad Dnd tests
        self.assertEqual(exp.URL_ROOT, self.bad_dnd.url_root)
        self.assertEqual("/api/Bad_Leaf_69_420", self.bad_dnd.url_leaf)
        self.assertEqual(exp.HEADERS, self.bad_dnd.requests_args["headers"])
        self.assertIsInstance(self.bad_dnd.df, pd.DataFrame)

        # TODO Refactor into property test methods
        self.assertEqual((24, 2), self.dnd.shape)
        self.assertIsInstance(self.dnd.url_column, pd.Series)
        self.assertIsInstance(self.dnd.name_column, pd.Series)
        self.assertRaises(RuntimeError, lambda: self.dnd.obj_column)
        self.assertEqual(48, self.dnd.size)

        self.maxDiff = None
        self.assertEqual(24, len(self.dnd.values))
        self.assertIsInstance(self.dnd.index, pd.Index)
        self.assertEqual(2, self.dnd.ndim)
        self.dnd.obj_column = self.dnd.url_column.rename("obj") * 0
        self.assertEqual((24, 3), self.dnd.shape)
        self.assertListEqual(['name', 'url', 'obj'], list(self.dnd.columns))
        self.dnd.obj_column = self.dnd.obj_column.rename(3)
        self.dnd.url_column = self.dnd.obj_column.rename(2)
        self.dnd.name_column = self.dnd.obj_column.rename(1)
        self.assertListEqual([1, 2, 3], list(self.dnd.columns))
        self.assertTrue((self.dnd == "").all().all())
        self.dnd.df = self.dnd.dframe
        self.assertTrue((self.dnd != "").all().all())

        self.assertEqual((1, 3), self.bad_dnd.shape)
        self.assertIsInstance(self.bad_dnd.url_column, pd.Series)
        self.assertIsInstance(self.bad_dnd.name_column, pd.Series)
        self.assertEqual(3, self.bad_dnd.size)

        self.maxDiff = None
        self.assertEqual(1, len(self.bad_dnd.values))
        self.assertIsInstance(self.bad_dnd.index, pd.Index)
        self.assertEqual(2, self.bad_dnd.ndim)

    def test_url_full(self):
        """tests url_full property

        Returns
        -------
        None
        """

        def invalid_assignment():
            """
            Raises
            ------
            AttributeError
            """
            self.dnd.url_full = None

        self.assertEqual("https://www.dnd5eapi.co/api", self.dnd.url_full)
        self.assertEqual(
            "https://www.dnd5eapi.co/api/Bad_Leaf_69_420", self.bad_dnd.url_full
        )
        self.assertRaises(AttributeError, invalid_assignment)

    def test_columns(self) -> None:
        """tests columns property

        Returns
        -------
        None
        """

        def invalid_type_assignment() -> None:
            """
            Raises
            ------
            AttributeError
            """
            self.dnd.columns = None

        def invalid_value_assignment() -> None:
            """
            Raises
            ------
            AttributeError
            """
            self.dnd.columns = [None]

        self.assertListEqual(['name', 'url'], list(self.dnd.columns))
        self.assertListEqual(['status_code', 'name', 'url'], list(self.bad_dnd.columns))
        self.assertRaises(TypeError, invalid_type_assignment)
        self.assertRaises(ValueError, invalid_value_assignment)
        self.dnd.columns = [NEW_NAME_COLUMN_NAME, NEW_URL_COLUMN_NAME]
        self.assertListEqual([NEW_NAME_COLUMN_NAME, NEW_URL_COLUMN_NAME], list(self.dnd.columns))
        self.assertEqual(NEW_NAME_COLUMN_NAME, self.dnd.name_column_name)
        self.assertEqual(NEW_URL_COLUMN_NAME, self.dnd.url_column_name)
        self.assertEqual("obj", self.dnd.obj_column_name)

    def test_obj_column_name(self):
        """tests obj_column_name property

        Returns
        -------
        None
        """
        # Good D&D Tests
        self.assertEqual("obj", self.dnd.obj_column_name)
        self.assertNotIn(self.dnd.obj_column_name, self.dnd.columns)
        self.dnd.obj_column_name = NEW_OBJ_COLUMN_NAME
        self.assertEqual(NEW_OBJ_COLUMN_NAME, self.dnd.obj_column_name)
        self.assertNotIn(self.dnd.obj_column_name, self.dnd.columns)
        # Bad D&D Tests
        self.assertEqual("obj", self.bad_dnd.obj_column_name)
        self.assertNotIn(self.bad_dnd.obj_column_name, self.bad_dnd.columns)
        self.bad_dnd.obj_column_name = NEW_OBJ_COLUMN_NAME
        self.assertEqual(NEW_OBJ_COLUMN_NAME, self.bad_dnd.obj_column_name)
        self.assertNotIn(self.bad_dnd.obj_column_name, self.bad_dnd.columns)

    def test_url_column_name(self):
        """tests url_column_name property

        Returns
        -------
        None
        """
        # Good D&D Tests
        self.assertEqual("url", self.dnd.url_column_name)
        self.assertIn(self.dnd.url_column_name, self.dnd.columns)
        self.dnd.url_column_name = NEW_URL_COLUMN_NAME
        self.assertEqual(NEW_URL_COLUMN_NAME, self.dnd.url_column_name)
        self.assertIn(self.dnd.url_column_name, self.dnd.columns)
        # Bad D&D Tests
        self.assertEqual("url", self.bad_dnd.url_column_name)
        self.assertIn(self.bad_dnd.url_column_name, self.bad_dnd.columns)
        self.bad_dnd.url_column_name = NEW_URL_COLUMN_NAME
        self.assertEqual(NEW_URL_COLUMN_NAME, self.bad_dnd.url_column_name)
        self.assertIn(self.bad_dnd.url_column_name, self.bad_dnd.columns)

    def test_name_column_name(self):
        """tests name_column_name property

        Returns
        -------
        None
        """
        # Good D&D Tests
        self.assertEqual("name", self.dnd.name_column_name)
        self.assertIn(self.dnd.name_column_name, self.dnd.columns)
        self.dnd.name_column_name = NEW_NAME_COLUMN_NAME
        self.assertEqual(NEW_NAME_COLUMN_NAME, self.dnd.name_column_name)
        self.assertIn(self.dnd.name_column_name, self.dnd.columns)
        # Bad D&D Tests
        self.assertEqual("name", self.bad_dnd.name_column_name)
        self.assertIn(self.bad_dnd.name_column_name, self.bad_dnd.columns)
        self.bad_dnd.name_column_name = NEW_NAME_COLUMN_NAME
        self.assertEqual(NEW_NAME_COLUMN_NAME, self.bad_dnd.name_column_name)
        self.assertIn(self.bad_dnd.name_column_name, self.bad_dnd.columns)

    def test_parents(self) -> None:
        """

        Returns
        -------

        """
        self.assertIsInstance(self.dnd, object)

    def test_children(self) -> None:
        """

        Returns
        -------

        """
        df_urls: NDArray[str] = self.dnd["url"].values
        cls_urls: Dict[str:Type[dnd5eapy.DnD5eAPIObj]] = {
            subclass_constructor.url_leaf: subclass_constructor for subclass_constructor in
            self.constructor.__subclasses__()
        }
        df_url: str
        for df_url in df_urls:
            self.assertIn(df_url, cls_urls)
            subclass: dnd5eapy.DnD5eAPIObj = cls_urls[df_url]()
            self.assertIsInstance(subclass, self.constructor)

    def test_create_instances_from_urls(self) -> None:
        """

        Returns
        -------

        """
        self.dnd.create_instances_from_urls()
        self.assertIn("obj", self.dnd.df.columns)
        self.dnd.df["obj"].apply(lambda x: self.assertIsInstance(x, self.constructor))
        self.assertWarns(ResourceWarning, self.bad_dnd.create_instances_from_urls)

    def test_apply(self) -> None:
        """

        Returns
        -------
        None
        """

        def func(_x: pd.Series) -> None:
            """

            Returns
            -------
            None
            """
            try:
                _ = [self.assertIn(_i, _x.index) for _i in ["url", "name"]]
                self.assertIn("/api/", _x["url"])
                self.assertEqual(f"/api/{_x['name'].lower().replace(' ', '-')}", _x["url"])
            except Exception as _e:
                print(_x)
                raise _e

        self.dnd.df.apply(func, axis=1)


class TestGetLeafConstructorMap(TestCase):
    """tests dnd5eapy.get_leaf_constructor_map

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.constructor = dnd5eapy.DnD5eAPIObj
        self.constructors_const = dnd5eapy.get_leaf_constructor_map

    def test_caller(self) -> None:
        """

        Returns
        -------

        """
        results = self.constructors_const()
        called = [const() for const in results.values()]
        _ = [self.assertIsInstance(obj, self.constructor) for obj in called]


class TestAbilityScores(TestCase):
    """Tests dnd5eapy.AbilityScores

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_ability_scores = dnd5eapy.AbilityScores(url_root=exp.URL_ROOT)

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_ability_scores.url_root)
        self.assertEqual("/api/ability-scores", self.dnd_ability_scores.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/ability-scores", self.dnd_ability_scores.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_ability_scores.requests_args["headers"])
        self.assertIsInstance(self.dnd_ability_scores.df, pd.DataFrame)
        self.assertEqual((6, 2), self.dnd_ability_scores.shape)

    def test_create_instances_from_urls(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_ability_scores.create_instances_from_urls()


# pylint: disable=E1101
class TestAbilityScore(TestCase):
    """Tests dnd5eapy.abilityscores

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_ability_score = dnd5eapy.AbilityScore()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_ability_score.url_root)
        self.assertEqual("/api/ability-scores/cha", self.dnd_ability_score.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/ability-scores/cha", self.dnd_ability_score.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_ability_score.requests_args["headers"])
        self.assertIsInstance(self.dnd_ability_score.df, pd.DataFrame)
        self.assertEqual((1, 5), self.dnd_ability_score.shape)
        self.assertListEqual(self.dnd_ability_score.columns.to_list(),
                             ['name', 'full_name', 'desc', 'skills', 'url'])
        self.assertEqual("CHA", self.dnd_ability_score.name)
        self.assertEqual("Charisma", self.dnd_ability_score.full_name)
        self.assertListEqual([
            'Charisma measures your ability to interact effectively with others. It includes such '
            'factors as confidence and eloquence, and it can represent a charming or commanding personality.',
            'A Charisma check might arise when you try to influence or entertain others, when you try to make an '
            'impression or tell a convincing lie, or when you are navigating a tricky social situation. '
            'The Deception, Intimidation, Performance, and Persuasion skills reflect aptitude in '
            'certain kinds of Charisma checks.'],
            list(self.dnd_ability_score.desc))
        self.assertIsInstance(self.dnd_ability_score.skills, dnd5eapy.Skills)


class TestAlignments(TestCase):
    """Tests dnd5eapy.Alignments

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_alignments = dnd5eapy.Alignments()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_alignments.url_root)
        self.assertEqual("/api/alignments", self.dnd_alignments.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/alignments", self.dnd_alignments.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_alignments.requests_args["headers"])
        self.assertIsInstance(self.dnd_alignments.df, pd.DataFrame)
        self.assertEqual((9, 2), self.dnd_alignments.shape)


class TestAlignment(TestCase):
    """Tests dnd5eapy.Alignments

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_alignment = dnd5eapy.Alignment()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_alignment.url_root)
        self.assertEqual("/api/alignments/chaotic-evil", self.dnd_alignment.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/alignments/chaotic-evil", self.dnd_alignment.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_alignment.requests_args["headers"])
        self.assertIsInstance(self.dnd_alignment.df, pd.DataFrame)
        self.assertEqual((1, 4), self.dnd_alignment.shape)
        self.assertListEqual(self.dnd_alignment.columns.to_list(), ['name', 'abbreviation', 'desc', 'url'])


class TestBackgrounds(TestCase):
    """Tests dnd5eapy.Backgrounds

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_backgrounds = dnd5eapy.Backgrounds()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_backgrounds.url_root)
        self.assertEqual("/api/backgrounds", self.dnd_backgrounds.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/backgrounds", self.dnd_backgrounds.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_backgrounds.requests_args["headers"])
        self.assertIsInstance(self.dnd_backgrounds.df, pd.DataFrame)
        self.assertEqual((1, 2), self.dnd_backgrounds.shape)


class TestBackground(TestCase):
    """Tests dnd5eapy.Background

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_background = dnd5eapy.Background()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_background.url_root)
        self.assertEqual('/api/backgrounds/acolyte', self.dnd_background.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/backgrounds/acolyte", self.dnd_background.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_background.requests_args["headers"])
        self.assertIsInstance(self.dnd_background.df, pd.DataFrame)
        self.assertEqual((1, 27), self.dnd_background.shape)
        self.maxDiff = None
        self.assertListEqual(self.dnd_background.columns.to_list(),
                             ['name', 'starting_proficiencies',
                              'starting_equipment', 'starting_equipment_options',
                              'url', 'language_options.choose',
                              'language_options.type', 'language_options.from.option_set_type',
                              'language_options.from.resource_list_url', 'feature.name',
                              'feature.desc', 'personality_traits.choose',
                              'personality_traits.type', 'personality_traits.from.option_set_type',
                              'personality_traits.from.options', 'ideals.choose',
                              'ideals.type', 'ideals.from.option_set_type',
                              'ideals.from.options', 'bonds.choose',
                              'bonds.type', 'bonds.from.option_set_type',
                              'bonds.from.options', 'flaws.choose',
                              'flaws.type', 'flaws.from.option_set_type',
                              'flaws.from.options'])


class TestClasses(TestCase):
    """Tests dnd5eapy.Classes

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_classes = dnd5eapy.Classes()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_classes.url_root)
        self.assertEqual("/api/classes", self.dnd_classes.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/classes", self.dnd_classes.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_classes.requests_args["headers"])
        self.assertIsInstance(self.dnd_classes.df, pd.DataFrame)
        self.assertEqual((12, 2), self.dnd_classes.shape)


class TestClass(TestCase):
    """Tests dnd5eapy.Class

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_class = dnd5eapy.Class()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_class.url_root)
        self.assertEqual("/api/classes/barbarian", self.dnd_class.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/classes/barbarian", self.dnd_class.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_class.requests_args["headers"])
        self.assertIsInstance(self.dnd_class.df, pd.DataFrame)
        self.assertEqual((1, 12), self.dnd_class.shape)
        self.maxDiff = None
        self.assertListEqual(self.dnd_class.columns.to_list(),
                             ['name', 'hit_die', 'proficiency_choices', 'proficiencies',
                              'saving_throws', 'starting_equipment', 'starting_equipment_options', 'class_levels',
                              'subclasses', 'url', 'multi_classing.prerequisites', 'multi_classing.proficiencies'])


class TestConditions(TestCase):
    """Tests dnd5eapy.Conditions
    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_conditions = dnd5eapy.Conditions()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_conditions.url_root)
        self.assertEqual("/api/conditions", self.dnd_conditions.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/conditions", self.dnd_conditions.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_conditions.requests_args["headers"])
        self.assertIsInstance(self.dnd_conditions.df, pd.DataFrame)
        self.assertEqual((15, 2), self.dnd_conditions.shape)


class TestCondition(TestCase):
    """Tests dnd5eapy.Condition
    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_condition = dnd5eapy.Condition()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_condition.url_root)
        self.assertEqual("/api/conditions/blinded", self.dnd_condition.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/conditions/blinded", self.dnd_condition.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_condition.requests_args["headers"])
        self.assertIsInstance(self.dnd_condition.df, pd.DataFrame)
        self.assertEqual((1, 3), self.dnd_condition.shape)
        self.assertListEqual(self.dnd_condition.columns.to_list(), ['name', 'desc', 'url'])


class TestDamageTypes(TestCase):
    """Tests dnd5eapy.DamageTypes
    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_damage_types = dnd5eapy.DamageTypes()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_damage_types.url_root)
        self.assertEqual("/api/damage-types", self.dnd_damage_types.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/damage-types", self.dnd_damage_types.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_damage_types.requests_args["headers"])
        self.assertIsInstance(self.dnd_damage_types.df, pd.DataFrame)
        self.assertEqual((13, 2), self.dnd_damage_types.shape)


class TestDamageType(TestCase):
    """Tests dnd5eapy.DamageType
    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_damage_type = dnd5eapy.DamageType()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_damage_type.url_root)
        self.assertEqual("/api/damage-types/acid", self.dnd_damage_type.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/damage-types/acid", self.dnd_damage_type.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_damage_type.requests_args["headers"])
        self.assertIsInstance(self.dnd_damage_type.df, pd.DataFrame)
        self.assertEqual((1, 3), self.dnd_damage_type.shape)
        self.assertListEqual(self.dnd_damage_type.columns.to_list(), ['name', 'desc', 'url'])


class TestEquipment(TestCase):
    """Tests dnd5eapy.Equipment

    """
    dnd_equipment: dnd5eapy.Equipment

    def setUp(self) -> None:
        """Tests dnd5eapy.Equipment

        Returns
        -------

        """
        self.dnd_equipment = dnd5eapy.Equipment()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_equipment.url_root)
        self.assertEqual("/api/equipment", self.dnd_equipment.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/equipment", self.dnd_equipment.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_equipment.requests_args["headers"])
        self.assertIsInstance(self.dnd_equipment.df, pd.DataFrame)
        self.assertEqual((237, 2), self.dnd_equipment.shape)


class TestEquipmentItem(TestCase):
    """Tests dnd5eapy.EquipmentItem

    """
    dnd_equipment_item: dnd5eapy.EquipmentItem

    def setUp(self) -> None:
        """Tests dnd5eapy.Equipment

        Returns
        -------

        """
        self.dnd_equipment_item = dnd5eapy.EquipmentItem()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_equipment_item.url_root)
        self.assertEqual("/api/equipment/abacus", self.dnd_equipment_item.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/equipment/abacus", self.dnd_equipment_item.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_equipment_item.requests_args["headers"])
        self.assertIsInstance(self.dnd_equipment_item.df, pd.DataFrame)
        self.assertEqual((1, 15), self.dnd_equipment_item.shape)
        self.assertListEqual(self.dnd_equipment_item.columns.to_list(),
                             ['desc', 'special', 'name', 'weight', 'url', 'contents',
                              'properties', 'equipment_category.index', 'equipment_category.name',
                              'equipment_category.url', 'gear_category.index', 'gear_category.name',
                              'gear_category.url', 'cost.quantity', 'cost.unit'])


class TestEquipmentCategories(TestCase):
    """Tests dnd5eapy.EquipmentCategories
    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_equipment_categories = dnd5eapy.EquipmentCategories()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_equipment_categories.url_root)
        self.assertEqual("/api/equipment-categories", self.dnd_equipment_categories.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/equipment-categories",
                         self.dnd_equipment_categories.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_equipment_categories.requests_args["headers"])
        self.assertIsInstance(self.dnd_equipment_categories.df, pd.DataFrame)
        self.assertEqual((39, 2), self.dnd_equipment_categories.shape)


class TestEquipmentCategory(TestCase):
    """Tests dnd5eapy.EquipmentCategory
    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_equipment_category = dnd5eapy.EquipmentCategory()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_equipment_category.url_root)
        self.assertEqual("/api/equipment-categories/adventuring-gear", self.dnd_equipment_category.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/equipment-categories/adventuring-gear",
                         self.dnd_equipment_category.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_equipment_category.requests_args["headers"])
        self.assertIsInstance(self.dnd_equipment_category.df, pd.DataFrame)
        self.assertEqual((1, 3), self.dnd_equipment_category.shape)
        self.assertListEqual(self.dnd_equipment_category.columns.to_list(), ['name', 'equipment', 'url'])


class TestFeats(TestCase):
    """Tests dnd5eapy.Feats
    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_feats = dnd5eapy.Feats()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_feats.url_root)
        self.assertEqual("/api/feats", self.dnd_feats.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/feats", self.dnd_feats.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_feats.requests_args["headers"])
        self.assertIsInstance(self.dnd_feats.df, pd.DataFrame)
        self.assertEqual((1, 2), self.dnd_feats.shape)


class TestFeat(TestCase):
    """Tests dnd5eapy.Feat
    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_feat = dnd5eapy.Feat()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_feat.url_root)
        self.assertEqual("/api/feats/grappler", self.dnd_feat.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/feats/grappler", self.dnd_feat.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_feat.requests_args["headers"])
        self.assertIsInstance(self.dnd_feat.df, pd.DataFrame)
        self.assertEqual((1, 4), self.dnd_feat.shape)
        self.assertListEqual(self.dnd_feat.columns.to_list(), ['name', 'prerequisites', 'desc', 'url'])


class TestFeatures(TestCase):
    """Tests dnd5eapy.Features

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_features = dnd5eapy.Features()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_features.url_root)
        self.assertEqual("/api/features", self.dnd_features.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/features", self.dnd_features.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_features.requests_args["headers"])
        self.assertIsInstance(self.dnd_features.df, pd.DataFrame)
        self.assertEqual((370, 2), self.dnd_features.shape)


class TestFeature(TestCase):
    """Tests dnd5eapy.Feature

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_feature = dnd5eapy.Feature()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_feature.url_root)
        self.assertEqual("/api/features/action-surge-1-use", self.dnd_feature.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/features/action-surge-1-use",
                         self.dnd_feature.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_feature.requests_args["headers"])
        self.assertIsInstance(self.dnd_feature.df, pd.DataFrame)
        self.assertEqual((1, 8), self.dnd_feature.shape)
        self.assertListEqual(self.dnd_feature.columns.to_list(),
                             ['name', 'level', 'prerequisites', 'desc', 'url', 'class.index', 'class.name',
                              'class.url'])


class TestLanguages(TestCase):
    """Tests dnd5eapy.Languages

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_languages = dnd5eapy.Languages()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_languages.url_root)
        self.assertEqual("/api/languages", self.dnd_languages.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/languages", self.dnd_languages.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_languages.requests_args["headers"])
        self.assertIsInstance(self.dnd_languages.df, pd.DataFrame)
        self.assertEqual((16, 2), self.dnd_languages.shape)


class TestLanguage(TestCase):
    """Tests dnd5eapy.Language

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_language = dnd5eapy.Language()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_language.url_root)
        self.assertEqual("/api/languages/abyssal", self.dnd_language.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/languages/abyssal", self.dnd_language.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_language.requests_args["headers"])
        self.assertIsInstance(self.dnd_language.df, pd.DataFrame)
        self.assertEqual((1, 5), self.dnd_language.shape)
        self.assertListEqual(self.dnd_language.columns.to_list(),
                             ['name', 'type', 'typical_speakers', 'script', 'url'])


class TestMagicItems(TestCase):
    """Tests dnd5eapy.MagicItems
    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_magic_items = dnd5eapy.MagicItems()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_magic_items.url_root)
        self.assertEqual("/api/magic-items", self.dnd_magic_items.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/magic-items", self.dnd_magic_items.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_magic_items.requests_args["headers"])
        self.assertIsInstance(self.dnd_magic_items.df, pd.DataFrame)
        self.assertEqual((362, 2), self.dnd_magic_items.shape)


class TestMagicItem(TestCase):
    """Tests dnd5eapy.MagicItem
    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_magic_item = dnd5eapy.MagicItem()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_magic_item.url_root)
        self.assertEqual("/api/magic-items/adamantine-armor", self.dnd_magic_item.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/magic-items/adamantine-armor",
                         self.dnd_magic_item.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_magic_item.requests_args["headers"])
        self.assertIsInstance(self.dnd_magic_item.df, pd.DataFrame)
        self.assertEqual((1, 9), self.dnd_magic_item.shape)
        self.assertListEqual(self.dnd_magic_item.columns.to_list(),
                             ['name', 'variants', 'variant', 'desc', 'url', 'equipment_category.index',
                              'equipment_category.name', 'equipment_category.url', 'rarity.name'])


class TestMagicSchools(TestCase):
    """Tests dnd5eapy.MagicSchools

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_magic_schools = dnd5eapy.MagicSchools()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_magic_schools.url_root)
        self.assertEqual("/api/magic-schools", self.dnd_magic_schools.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/magic-schools", self.dnd_magic_schools.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_magic_schools.requests_args["headers"])
        self.assertIsInstance(self.dnd_magic_schools.df, pd.DataFrame)
        self.assertEqual((8, 2), self.dnd_magic_schools.shape)


class TestMagicSchool(TestCase):
    """Tests dnd5eapy.MagicSchool

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_magic_school = dnd5eapy.MagicSchool()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_magic_school.url_root)
        self.assertEqual("/api/magic-schools/abjuration", self.dnd_magic_school.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/magic-schools/abjuration",
                         self.dnd_magic_school.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_magic_school.requests_args["headers"])
        self.assertIsInstance(self.dnd_magic_school.df, pd.DataFrame)
        self.assertEqual((1, 3), self.dnd_magic_school.shape)
        self.assertListEqual(self.dnd_magic_school.columns.to_list(), ['name', 'desc', 'url'])


class TestMonsters(TestCase):
    """Tests dnd5eapy.Monsters

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_monsters = dnd5eapy.Monsters()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_monsters.url_root)
        self.assertEqual("/api/monsters", self.dnd_monsters.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/monsters", self.dnd_monsters.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_monsters.requests_args["headers"])
        self.assertIsInstance(self.dnd_monsters.df, pd.DataFrame)
        self.assertEqual((334, 2), self.dnd_monsters.shape)


class TestMonster(TestCase):
    """Tests dnd5eapy.Monster

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_monster = dnd5eapy.Monster()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_monster.url_root)
        self.assertEqual("/api/monsters/aboleth", self.dnd_monster.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/monsters/aboleth", self.dnd_monster.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_monster.requests_args["headers"])
        self.assertIsInstance(self.dnd_monster.df, pd.DataFrame)
        self.assertEqual((1, 32), self.dnd_monster.shape)
        self.assertListEqual(self.dnd_monster.columns.to_list(),
                             ['name', 'size', 'type', 'alignment', 'armor_class', 'hit_points', 'hit_dice',
                              'hit_points_roll', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom',
                              'charisma', 'proficiencies', 'damage_vulnerabilities', 'damage_resistances',
                              'damage_immunities', 'condition_immunities', 'languages', 'challenge_rating',
                              'proficiency_bonus', 'xp', 'special_abilities', 'actions', 'legendary_actions', 'image',
                              'url', 'speed.walk', 'speed.swim', 'senses.darkvision', 'senses.passive_perception'])


class TestProficiencies(TestCase):
    """Tests dnd5eapy.Proficiencies

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_proficiencies = dnd5eapy.Proficiencies()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_proficiencies.url_root)
        self.assertEqual("/api/proficiencies", self.dnd_proficiencies.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/proficiencies", self.dnd_proficiencies.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_proficiencies.requests_args["headers"])
        self.assertIsInstance(self.dnd_proficiencies.df, pd.DataFrame)
        self.assertEqual((117, 2), self.dnd_proficiencies.shape)


class TestProficiency(TestCase):
    """Tests dnd5eapy.Proficiency

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_proficiency = dnd5eapy.Proficiency()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_proficiency.url_root)
        self.assertEqual("/api/proficiencies/alchemists-supplies", self.dnd_proficiency.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/proficiencies/alchemists-supplies",
                         self.dnd_proficiency.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_proficiency.requests_args["headers"])
        self.assertIsInstance(self.dnd_proficiency.df, pd.DataFrame)
        self.assertEqual((1, 8), self.dnd_proficiency.shape)
        self.maxDiff = None
        self.assertListEqual(self.dnd_proficiency.columns.to_list(),
                             ['type', 'name', 'classes', 'races', 'url', 'reference.index', 'reference.name',
                              'reference.url'])


class TestRaces(TestCase):
    """Tests dnd5eapy.Races

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_races = dnd5eapy.Races()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_races.url_root)
        self.assertEqual("/api/races", self.dnd_races.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/races", self.dnd_races.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_races.requests_args["headers"])
        self.assertIsInstance(self.dnd_races.df, pd.DataFrame)
        self.assertEqual((9, 2), self.dnd_races.shape)


class TestRace(TestCase):
    """Tests dnd5eapy.Race

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_race = dnd5eapy.Race()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_race.url_root)
        self.assertEqual("/api/races/dragonborn", self.dnd_race.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/races/dragonborn", self.dnd_race.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_race.requests_args["headers"])
        self.assertIsInstance(self.dnd_race.df, pd.DataFrame)
        self.assertEqual((1, 13), self.dnd_race.shape)
        self.assertListEqual(self.dnd_race.columns.to_list(),
                             ['name', 'speed', 'ability_bonuses', 'alignment', 'age', 'size', 'size_description',
                              'starting_proficiencies', 'languages', 'language_desc', 'traits', 'subraces', 'url'])


class TestRuleSections(TestCase):
    """Tests dnd5eapy.RuleSections

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_rule_sections = dnd5eapy.RuleSections()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_rule_sections.url_root)
        self.assertEqual("/api/rule-sections", self.dnd_rule_sections.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/rule-sections", self.dnd_rule_sections.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_rule_sections.requests_args["headers"])
        self.assertIsInstance(self.dnd_rule_sections.df, pd.DataFrame)
        self.assertEqual((33, 2), self.dnd_rule_sections.shape)


class TestRuleSection(TestCase):
    """Tests dnd5eapy.RuleSection

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_rule_section = dnd5eapy.RuleSection()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_rule_section.url_root)
        self.assertEqual("/api/rule-sections/ability-checks", self.dnd_rule_section.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/rule-sections/ability-checks",
                         self.dnd_rule_section.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_rule_section.requests_args["headers"])
        self.assertIsInstance(self.dnd_rule_section.df, pd.DataFrame)
        self.assertEqual((1, 3), self.dnd_rule_section.shape)
        self.assertListEqual(self.dnd_rule_section.columns.to_list(), ['name', 'desc', 'url'])


class TestRules(TestCase):
    """Tests dnd5eapy.Rules

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_rules = dnd5eapy.Rules()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_rules.url_root)
        self.assertEqual("/api/rules", self.dnd_rules.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/rules", self.dnd_rules.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_rules.requests_args["headers"])
        self.assertIsInstance(self.dnd_rules.df, pd.DataFrame)
        self.assertEqual((6, 2), self.dnd_rules.shape)


class TestRule(TestCase):
    """Tests dnd5eapy.Rule

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_rule = dnd5eapy.Rule()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_rule.url_root)
        self.assertEqual("/api/rules/adventuring", self.dnd_rule.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/rules/adventuring", self.dnd_rule.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_rule.requests_args["headers"])
        self.assertIsInstance(self.dnd_rule.df, pd.DataFrame)
        self.assertEqual((1, 4), self.dnd_rule.shape)
        self.assertListEqual(self.dnd_rule.columns.to_list(), ['name', 'desc', 'subsections', 'url'])


class TestSkills(TestCase):
    """Tests dnd5eapy.Skills

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_skills = dnd5eapy.Skills()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_skills.url_root)
        self.assertEqual("/api/skills", self.dnd_skills.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/skills", self.dnd_skills.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_skills.requests_args["headers"])
        self.assertIsInstance(self.dnd_skills.df, pd.DataFrame)
        self.assertEqual((18, 2), self.dnd_skills.shape)


class TestSkill(TestCase):
    """Tests dnd5eapy.Skill

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_skill = dnd5eapy.Skill()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_skill.url_root)
        self.assertEqual("/api/skills/acrobatics", self.dnd_skill.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/skills/acrobatics", self.dnd_skill.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_skill.requests_args["headers"])
        self.assertIsInstance(self.dnd_skill.df, pd.DataFrame)
        self.assertEqual((1, 6), self.dnd_skill.shape)
        self.assertListEqual(self.dnd_skill.columns.to_list(),
                             ['name', 'desc', 'url', 'ability_score.index', 'ability_score.name',
                              'ability_score.url'])


class TestSpells(TestCase):
    """Tests dnd5eapy.Spells

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_spells = dnd5eapy.Spells()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_spells.url_root)
        self.assertEqual("/api/spells", self.dnd_spells.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/spells", self.dnd_spells.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_spells.requests_args["headers"])
        self.assertIsInstance(self.dnd_spells.df, pd.DataFrame)
        self.assertEqual((319, 2), self.dnd_spells.shape)


class TestSpell(TestCase):
    """Tests dnd5eapy.Spell

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_spell = dnd5eapy.Spell()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_spell.url_root)
        self.assertEqual("/api/spells/acid-arrow", self.dnd_spell.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/spells/acid-arrow", self.dnd_spell.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_spell.requests_args["headers"])
        self.assertIsInstance(self.dnd_spell.df, pd.DataFrame)
        self.assertEqual((1, 29), self.dnd_spell.shape)
        self.maxDiff = None
        self.assertListEqual(self.dnd_spell.columns.to_list(),
                             ['name', 'desc', 'higher_level', 'range', 'components', 'material', 'ritual', 'duration',
                              'concentration', 'casting_time', 'level', 'attack_type', 'classes', 'subclasses',
                              'url',
                              'damage.damage_type.index', 'damage.damage_type.name', 'damage.damage_type.url',
                              'damage.damage_at_slot_level.2', 'damage.damage_at_slot_level.3',
                              'damage.damage_at_slot_level.4', 'damage.damage_at_slot_level.5',
                              'damage.damage_at_slot_level.6', 'damage.damage_at_slot_level.7',
                              'damage.damage_at_slot_level.8', 'damage.damage_at_slot_level.9', 'school.index',
                              'school.name', 'school.url'])


class TestSubclasses(TestCase):
    """Tests dnd5eapy.Subclasses

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_subclasses = dnd5eapy.Subclasses()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_subclasses.url_root)
        self.assertEqual("/api/subclasses", self.dnd_subclasses.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/subclasses", self.dnd_subclasses.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_subclasses.requests_args["headers"])
        self.assertIsInstance(self.dnd_subclasses.df, pd.DataFrame)
        self.assertEqual((12, 2), self.dnd_subclasses.shape)


class TestSubclass(TestCase):
    """Tests dnd5eapy.Subclass

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_subclass = dnd5eapy.Subclass()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_subclass.url_root)
        self.assertEqual("/api/subclasses/berserker", self.dnd_subclass.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/subclasses/berserker", self.dnd_subclass.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_subclass.requests_args["headers"])
        self.assertIsInstance(self.dnd_subclass.df, pd.DataFrame)
        self.assertEqual((1, 9), self.dnd_subclass.shape)
        self.assertListEqual(self.dnd_subclass.columns.to_list(),
                             ['name', 'subclass_flavor', 'desc', 'subclass_levels', 'url', 'spells', 'class.index',
                              'class.name', 'class.url'])


class TestSubraces(TestCase):
    """Tests dnd5eapy.Subraces

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_subraces = dnd5eapy.Subraces()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_subraces.url_root)
        self.assertEqual("/api/subraces", self.dnd_subraces.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/subraces", self.dnd_subraces.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_subraces.requests_args["headers"])
        self.assertIsInstance(self.dnd_subraces.df, pd.DataFrame)
        self.assertEqual((4, 2), self.dnd_subraces.shape)


class TestSubrace(TestCase):
    """Tests dnd5eapy.Subrace

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_subrace = dnd5eapy.Subrace()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_subrace.url_root)
        self.assertEqual("/api/subraces/high-elf", self.dnd_subrace.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/subraces/high-elf", self.dnd_subrace.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_subrace.requests_args["headers"])
        self.assertIsInstance(self.dnd_subrace.df, pd.DataFrame)
        self.assertEqual((1, 14), self.dnd_subrace.shape)
        self.assertListEqual(self.dnd_subrace.columns.to_list(),
                             ['name', 'desc', 'ability_bonuses', 'starting_proficiencies', 'languages', 'racial_traits',
                              'url', 'race.index', 'race.name', 'race.url', 'language_options.choose',
                              'language_options.from.option_set_type', 'language_options.from.options',
                              'language_options.type'])


class TestTraits(TestCase):
    """Tests dnd5eapy.Traits

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_traits = dnd5eapy.Traits()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_traits.url_root)
        self.assertEqual("/api/traits", self.dnd_traits.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/traits", self.dnd_traits.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_traits.requests_args["headers"])
        self.assertIsInstance(self.dnd_traits.df, pd.DataFrame)
        self.assertEqual((38, 2), self.dnd_traits.shape)


class TestTrait(TestCase):
    """Tests dnd5eapy.Trait

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_trait = dnd5eapy.Trait()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(exp.URL_ROOT, self.dnd_trait.url_root)
        self.assertEqual("/api/traits/artificers-lore", self.dnd_trait.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/traits/artificers-lore", self.dnd_trait.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_trait.requests_args["headers"])
        self.assertIsInstance(self.dnd_trait.df, pd.DataFrame)
        self.assertEqual((1, 6), self.dnd_trait.shape)
        self.assertListEqual(self.dnd_trait.columns.to_list(),
                             ['races', 'subraces', 'name', 'desc', 'proficiencies', 'url'])


class TestWeaponProperties(TestCase):
    """Tests dnd5eapy.WeaponProperties

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_weapon_properties = dnd5eapy.WeaponProperties()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual("https://www.dnd5eapi.co", self.dnd_weapon_properties.url_root)
        self.assertEqual("/api/weapon-properties", self.dnd_weapon_properties.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/weapon-properties",
                         self.dnd_weapon_properties.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_weapon_properties.requests_args["headers"])
        self.assertIsInstance(self.dnd_weapon_properties.df, pd.DataFrame)
        self.assertEqual((11, 2), self.dnd_weapon_properties.shape)


class TestWeaponProperty(TestCase):
    """Tests dnd5eapy.WeaponProperty

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_weapon_property = dnd5eapy.WeaponProperty()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual("https://www.dnd5eapi.co", self.dnd_weapon_property.url_root)
        self.assertEqual("/api/weapon-properties/ammunition", self.dnd_weapon_property.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/weapon-properties/ammunition",
                         self.dnd_weapon_property.url_full)
        self.assertEqual(exp.HEADERS, self.dnd_weapon_property.requests_args["headers"])
        self.assertIsInstance(self.dnd_weapon_property.df, pd.DataFrame)
        self.assertEqual((1, 3), self.dnd_weapon_property.shape)
        self.assertListEqual(self.dnd_weapon_property.columns.to_list(), ['name', 'desc', 'url'])
