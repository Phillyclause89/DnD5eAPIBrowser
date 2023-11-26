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

"""dnd5eapy module for easy transfer of dnd5eapi.co to pandas.DataFrame

Under development python library for working with https://www.dnd5eapi.co/api responses in python.

"""

from dnd5eapy.core import DnD5eAPIObj, get_leaf_constructor_map
from dnd5eapy.abilityscores import AbilityScores, AbilityScore
from dnd5eapy.alignments import Alignments, Alignment
from dnd5eapy.backgrounds import Backgrounds, Background
from dnd5eapy.classes import Classes, Class
from dnd5eapy.conditions import Conditions, Condition
from dnd5eapy.damagetypes import DamageTypes, DamageType
from dnd5eapy.equipment import Equipment, EquipmentItem
from dnd5eapy.equipmentcategories import EquipmentCategories, EquipmentCategory
from dnd5eapy.feats import Feats, Feat
from dnd5eapy.features import Features, Feature
from dnd5eapy.languages import Languages, Language
from dnd5eapy.magicitems import MagicItems, MagicItem
from dnd5eapy.magicschools import MagicSchools, MagicSchool
from dnd5eapy.monsters import Monsters, Monster
from dnd5eapy.proficiencies import Proficiencies, Proficiency
from dnd5eapy.races import Races, Race
from dnd5eapy.rules import Rules, Rule
from dnd5eapy.rulesections import RuleSections, RuleSection
from dnd5eapy.skills import Skills, Skill
from dnd5eapy.spells import Spells, Spell
from dnd5eapy.subraces import Subraces, Subrace
from dnd5eapy.subclasses import Subclasses, Subclass
from dnd5eapy.traits import Traits, Trait
from dnd5eapy.weaponproperties import WeaponProperty, WeaponProperties

__all__ = [
    "get_leaf_constructor_map", "DnD5eAPIObj",
    "AbilityScores", "AbilityScore",
    "Alignments", "Alignment",
    "Backgrounds", "Background",
    "Classes", "Class",
    "Conditions", "Condition",
    "DamageTypes", "DamageType",
    "Equipment", "EquipmentItem",
    "EquipmentCategories", "EquipmentCategory",
    "Feats", "Feat",
    "Features", "Feature",
    "Languages", "Language",
    "MagicItems", "MagicItem",
    "MagicSchools", "MagicSchool",
    "Monsters", "Monster",
    "Proficiencies", "Proficiency",
    "Races", "Race",
    "Rules", "Rule",
    "RuleSections", "RuleSection",
    "Skills", "Skill",
    "Spells", "Spell",
    "Subclasses", "Subclass",
    "Subraces", "Subrace",
]
