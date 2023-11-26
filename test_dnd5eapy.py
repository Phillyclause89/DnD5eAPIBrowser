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
"""tests for dnd5eapy

"""

from typing import Any, Dict, List, Type, Union
from unittest import TestCase

import pandas as pd
from numpy.typing import NDArray
from pandas import DataFrame

import dnd5eapy

URL_ROOT = "https://www.dnd5eapi.co"

HEADERS = {'Accept': 'application/json'}

GOOD_BASE_RESPONSE: Dict[str, str] = {'ability-scores': '/api/ability-scores',
                                      'alignments': '/api/alignments',
                                      'backgrounds': '/api/backgrounds',
                                      'classes': '/api/classes',
                                      'conditions': '/api/conditions',
                                      'damage-types': '/api/damage-types',
                                      'equipment': '/api/equipment',
                                      'equipment-categories': '/api/equipment-categories',
                                      'feats': '/api/feats',
                                      'features': '/api/features',
                                      'languages': '/api/languages',
                                      'magic-items': '/api/magic-items',
                                      'magic-schools': '/api/magic-schools',
                                      'monsters': '/api/monsters',
                                      'proficiencies': '/api/proficiencies',
                                      'races': '/api/races',
                                      'rule-sections': '/api/rule-sections',
                                      'rules': '/api/rules',
                                      'skills': '/api/skills',
                                      'spells': '/api/spells',
                                      'subclasses': '/api/subclasses',
                                      'subraces': '/api/subraces',
                                      'traits': '/api/traits',
                                      'weapon-properties': '/api/weapon-properties'}
BAD_404_RESPONSE: Dict[str, int] = {'status_code': 404}
ABILITY_SCORES_RESPONSE: Dict[str, Union[int, List[
    Union[Dict[str, str], Dict[str, str], Dict[str, str],
          Dict[str, str], Dict[str, str], Dict[str, str]]]]] = {
    'count': 6,
    'results': [{'index': 'cha', 'name': 'CHA', 'url': '/api/ability-scores/cha'},
                {'index': 'con', 'name': 'CON', 'url': '/api/ability-scores/con'},
                {'index': 'dex', 'name': 'DEX', 'url': '/api/ability-scores/dex'},
                {'index': 'int', 'name': 'INT', 'url': '/api/ability-scores/int'},
                {'index': 'str', 'name': 'STR', 'url': '/api/ability-scores/str'},
                {'index': 'wis', 'name': 'WIS', 'url': '/api/ability-scores/wis'}]}
ABILITY_SCORE_RESPONSE: Dict[
    str, Union[str, List[Union[Dict[str, str], Dict[str, str],
                               Dict[str, str], Dict[str, str]]], List[str]]] = {
    'desc': ['Charisma measures your ability to interact effectively with others. '
             'It includes such factors as confidence and eloquence, and it can '
             'represent a charming or commanding personality.',
             'A Charisma check might arise when you try to influence or entertain '
             'others, when you try to make an impression or tell a convincing '
             'lie, or when you are navigating a tricky social situation. The '
             'Deception, Intimidation, Performance, and Persuasion skills reflect '
             'aptitude in certain kinds of Charisma checks.'],
    'full_name': 'Charisma',
    'index': 'cha',
    'name': 'CHA',
    'skills': [{'index': 'deception',
                'name': 'Deception',
                'url': '/api/skills/deception'},
               {'index': 'intimidation',
                'name': 'Intimidation',
                'url': '/api/skills/intimidation'},
               {'index': 'performance',
                'name': 'Performance',
                'url': '/api/skills/performance'},
               {'index': 'persuasion',
                'name': 'Persuasion',
                'url': '/api/skills/persuasion'}],
    'url': '/api/ability-scores/cha'}
ALIGNMENTS_RESPONSE: Dict[str, Union[int, List[Union[
    Dict[str, str], Dict[str, str], Dict[str, str],
    Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str],
    Dict[str, str], Dict[str, str]]]]
] = {'count': 9,
     'results': [{'index': 'chaotic-evil',
                  'name': 'Chaotic Evil',
                  'url': '/api/alignments/chaotic-evil'},
                 {'index': 'chaotic-good',
                  'name': 'Chaotic Good',
                  'url': '/api/alignments/chaotic-good'},
                 {'index': 'chaotic-neutral',
                  'name': 'Chaotic Neutral',
                  'url': '/api/alignments/chaotic-neutral'},
                 {'index': 'lawful-evil',
                  'name': 'Lawful Evil',
                  'url': '/api/alignments/lawful-evil'},
                 {'index': 'lawful-good',
                  'name': 'Lawful Good',
                  'url': '/api/alignments/lawful-good'},
                 {'index': 'lawful-neutral',
                  'name': 'Lawful Neutral',
                  'url': '/api/alignments/lawful-neutral'},
                 {'index': 'neutral',
                  'name': 'Neutral',
                  'url': '/api/alignments/neutral'},
                 {'index': 'neutral-evil',
                  'name': 'Neutral Evil',
                  'url': '/api/alignments/neutral-evil'},
                 {'index': 'neutral-good',
                  'name': 'Neutral Good',
                  'url': '/api/alignments/neutral-good'}]}
BACKGROUNDS_RESPONSE: Dict[
    str, Union[int, List[Dict[str, str]]]
] = {'count': 1,
     'results': [{'index': 'acolyte',
                  'name': 'Acolyte',
                  'url': '/api/backgrounds/acolyte'}]}
CLASSES_RESPONSE: Dict[str, Union[int, List[
    Union[Union[Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str]], Any]]]
] = {'count': 12,
     'results': [{
         'index': 'barbarian',
         'name': 'Barbarian',
         'url': '/api/classes/barbarian'},
         {
             'index': 'bard',
             'name': 'Bard',
             'url': '/api/classes/bard'},
         {
             'index': 'cleric',
             'name': 'Cleric',
             'url': '/api/classes/cleric'},
         {
             'index': 'druid',
             'name': 'Druid',
             'url': '/api/classes/druid'},
         {
             'index': 'fighter',
             'name': 'Fighter',
             'url': '/api/classes/fighter'},
         {
             'index': 'monk',
             'name': 'Monk',
             'url': '/api/classes/monk'},
         {
             'index': 'paladin',
             'name': 'Paladin',
             'url': '/api/classes/paladin'},
         {
             'index': 'ranger',
             'name': 'Ranger',
             'url': '/api/classes/ranger'},
         {
             'index': 'rogue',
             'name': 'Rogue',
             'url': '/api/classes/rogue'},
         {
             'index': 'sorcerer',
             'name': 'Sorcerer',
             'url': '/api/classes/sorcerer'},
         {
             'index': 'warlock',
             'name': 'Warlock',
             'url': '/api/classes/warlock'},
         {
             'index': 'wizard',
             'name': 'Wizard',
             'url': '/api/classes/wizard'}]}
CONDITIONS_RESPONSE: Dict[str, Union[int, List[
    Union[Union[Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str]], Any]]]
] = {'count': 15,
     'results': [{
         'index': 'blinded',
         'name': 'Blinded',
         'url': '/api/conditions/blinded'},
         {
             'index': 'charmed',
             'name': 'Charmed',
             'url': '/api/conditions/charmed'},
         {
             'index': 'deafened',
             'name': 'Deafened',
             'url': '/api/conditions/deafened'},
         {
             'index': 'exhaustion',
             'name': 'Exhaustion',
             'url': '/api/conditions/exhaustion'},
         {
             'index': 'frightened',
             'name': 'Frightened',
             'url': '/api/conditions/frightened'},
         {
             'index': 'grappled',
             'name': 'Grappled',
             'url': '/api/conditions/grappled'},
         {
             'index': 'incapacitated',
             'name': 'Incapacitated',
             'url': '/api/conditions/incapacitated'},
         {
             'index': 'invisible',
             'name': 'Invisible',
             'url': '/api/conditions/invisible'},
         {
             'index': 'paralyzed',
             'name': 'Paralyzed',
             'url': '/api/conditions/paralyzed'},
         {
             'index': 'petrified',
             'name': 'Petrified',
             'url': '/api/conditions/petrified'},
         {
             'index': 'poisoned',
             'name': 'Poisoned',
             'url': '/api/conditions/poisoned'},
         {
             'index': 'prone',
             'name': 'Prone',
             'url': '/api/conditions/prone'},
         {
             'index': 'restrained',
             'name': 'Restrained',
             'url': '/api/conditions/restrained'},
         {
             'index': 'stunned',
             'name': 'Stunned',
             'url': '/api/conditions/stunned'},
         {
             'index': 'unconscious',
             'name': 'Unconscious',
             'url': '/api/conditions/unconscious'}]}
DAMAGE_TYPES_RESPONSE: Dict[str, Union[int, List[
    Union[Union[Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str]], Any]]]
] = {'count': 13,
     'results': [{'index': 'acid',
                  'name': 'Acid',
                  'url': '/api/damage-types/acid'},
                 {
                     'index': 'bludgeoning',
                     'name': 'Bludgeoning',
                     'url': '/api/damage-types/bludgeoning'},
                 {'index': 'cold',
                  'name': 'Cold',
                  'url': '/api/damage-types/cold'},
                 {'index': 'fire',
                  'name': 'Fire',
                  'url': '/api/damage-types/fire'},
                 {'index': 'force',
                  'name': 'Force',
                  'url': '/api/damage-types/force'},
                 {
                     'index': 'lightning',
                     'name': 'Lightning',
                     'url': '/api/damage-types/lightning'},
                 {
                     'index': 'necrotic',
                     'name': 'Necrotic',
                     'url': '/api/damage-types/necrotic'},
                 {
                     'index': 'piercing',
                     'name': 'Piercing',
                     'url': '/api/damage-types/piercing'},
                 {'index': 'poison',
                  'name': 'Poison',
                  'url': '/api/damage-types/poison'},
                 {'index': 'psychic',
                  'name': 'Psychic',
                  'url': '/api/damage-types/psychic'},
                 {'index': 'radiant',
                  'name': 'Radiant',
                  'url': '/api/damage-types/radiant'},
                 {
                     'index': 'slashing',
                     'name': 'Slashing',
                     'url': '/api/damage-types/slashing'},
                 {'index': 'thunder',
                  'name': 'Thunder',
                  'url': '/api/damage-types/thunder'}]}
EQUIPMENT_RESPONSE: Dict[
    str, Union[int, List[Dict[str, str]]]
] = {'count': 237, 'results': [{
    'index': "abacus", 'name': "Abacus", 'url': "/api/equipment/abacus"
}]}
EQUIPMENT_CATEGORIES_RESPONSE: Dict[str, Union[int, List[
    Union[Union[Dict[str, str], Dict[str, str], Dict[str, str], Dict[
        str, str], Dict[str, str], Dict[str, str], Dict[
                    str, str], Dict[str, str], Dict[str, str], Dict[
                    str, str]], Any]]]
] = {'count': 39,
     'results': [{
         'index': 'adventuring-gear',
         'name': 'Adventuring Gear',
         'url': '/api/equipment-categories/adventuring-gear'},
         {
             'index': 'ammunition',
             'name': 'Ammunition',
             'url': '/api/equipment-categories/ammunition'},
         {
             'index': 'arcane-foci',
             'name': 'Arcane Foci',
             'url': '/api/equipment-categories/arcane-foci'},
         {
             'index': 'armor',
             'name': 'Armor',
             'url': '/api/equipment-categories/armor'},
         {
             'index': 'artisans-tools',
             'name': "Artisan's Tools",
             'url': '/api/equipment-categories/artisans-tools'},
         {
             'index': 'druidic-foci',
             'name': 'Druidic Foci',
             'url': '/api/equipment-categories/druidic-foci'},
         {
             'index': 'equipment-packs',
             'name': 'Equipment Packs',
             'url': '/api/equipment-categories/equipment-packs'},
         {
             'index': 'gaming-sets',
             'name': 'Gaming Sets',
             'url': '/api/equipment-categories/gaming-sets'},
         {
             'index': 'heavy-armor',
             'name': 'Heavy Armor',
             'url': '/api/equipment-categories/heavy-armor'},
         {
             'index': 'holy-symbols',
             'name': 'Holy Symbols',
             'url': '/api/equipment-categories/holy-symbols'},
         {
             'index': 'kits',
             'name': 'Kits',
             'url': '/api/equipment-categories/kits'},
         {
             'index': 'land-vehicles',
             'name': 'Land Vehicles',
             'url': '/api/equipment-categories/land-vehicles'},
         {
             'index': 'light-armor',
             'name': 'Light Armor',
             'url': '/api/equipment-categories/light-armor'},
         {
             'index': 'martial-melee-weapons',
             'name': 'Martial Melee Weapons',
             'url': '/api/equipment-categories/martial-melee-weapons'},
         {
             'index': 'martial-ranged-weapons',
             'name': 'Martial Ranged Weapons',
             'url': '/api/equipment-categories/martial-ranged-weapons'},
         {
             'index': 'martial-weapons',
             'name': 'Martial Weapons',
             'url': '/api/equipment-categories/martial-weapons'},
         {
             'index': 'medium-armor',
             'name': 'Medium Armor',
             'url': '/api/equipment-categories/medium-armor'},
         {
             'index': 'melee-weapons',
             'name': 'Melee Weapons',
             'url': '/api/equipment-categories/melee-weapons'},
         {
             'index': 'mounts-and-other-animals',
             'name': 'Mounts and Other Animals',
             'url': '/api/equipment-categories/mounts-and-other-animals'},
         {
             'index': 'mounts-and-vehicles',
             'name': 'Mounts and Vehicles',
             'url': '/api/equipment-categories/mounts-and-vehicles'},
         {
             'index': 'musical-instruments',
             'name': 'Musical Instruments',
             'url': '/api/equipment-categories/musical-instruments'},
         {
             'index': 'other-tools',
             'name': 'Other Tools',
             'url': '/api/equipment-categories/other-tools'},
         {
             'index': 'potion',
             'name': 'Potion',
             'url': '/api/equipment-categories/potion'},
         {
             'index': 'ranged-weapons',
             'name': 'Ranged Weapons',
             'url': '/api/equipment-categories/ranged-weapons'},
         {
             'index': 'ring',
             'name': 'Ring',
             'url': '/api/equipment-categories/ring'},
         {
             'index': 'rod',
             'name': 'Rod',
             'url': '/api/equipment-categories/rod'},
         {
             'index': 'scroll',
             'name': 'Scroll',
             'url': '/api/equipment-categories/scroll'},
         {
             'index': 'shields',
             'name': 'Shields',
             'url': '/api/equipment-categories/shields'},
         {
             'index': 'simple-melee-weapons',
             'name': 'Simple Melee Weapons',
             'url': '/api/equipment-categories/simple-melee-weapons'},
         {
             'index': 'simple-ranged-weapons',
             'name': 'Simple Ranged Weapons',
             'url': '/api/equipment-categories/simple-ranged-weapons'},
         {
             'index': 'simple-weapons',
             'name': 'Simple Weapons',
             'url': '/api/equipment-categories/simple-weapons'},
         {
             'index': 'staff',
             'name': 'Staff',
             'url': '/api/equipment-categories/staff'},
         {
             'index': 'standard-gear',
             'name': 'Standard Gear',
             'url': '/api/equipment-categories/standard-gear'},
         {
             'index': 'tack-harness-and-drawn-vehicles',
             'name': 'Tack, Harness, and Drawn Vehicles',
             'url': '/api/equipment-categories/tack-harness-and-drawn-vehicles'},
         {
             'index': 'tools',
             'name': 'Tools',
             'url': '/api/equipment-categories/tools'},
         {
             'index': 'wand',
             'name': 'Wand',
             'url': '/api/equipment-categories/wand'},
         {
             'index': 'waterborne-vehicles',
             'name': 'Waterborne Vehicles',
             'url': '/api/equipment-categories/waterborne-vehicles'},
         {
             'index': 'weapon',
             'name': 'Weapon',
             'url': '/api/equipment-categories/weapon'},
         {
             'index': 'wondrous-items',
             'name': 'Wondrous Items',
             'url': '/api/equipment-categories/wondrous-items'}]}
FEATS_RESPONSE: Dict[str, Union[int, List[Dict[str, str]]]
] = {'count': 1,
     'results': [{'index': 'grappler',
                  'name': 'Grappler',
                  'url': '/api/feats/grappler'}]}
FEATURES_RESPONSE: Dict[str, Union[int, List[Dict[str, str]]]
] = {'count': 370, 'results': [
    {"index": "action-surge-1-use",
     "name": "Action Surge (1 use)",
     "url": "/api/features/action-surge-1-use"}]}
LANGUAGES_RESPONSE: Dict[str, Union[int, List[
    Union[Union[Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str]], Any]]]
] = {'count': 16,
     'results': [{
         'index': 'abyssal',
         'name': 'Abyssal',
         'url': '/api/languages/abyssal'},
         {
             'index': 'celestial',
             'name': 'Celestial',
             'url': '/api/languages/celestial'},
         {
             'index': 'common',
             'name': 'Common',
             'url': '/api/languages/common'},
         {
             'index': 'deep-speech',
             'name': 'Deep Speech',
             'url': '/api/languages/deep-speech'},
         {
             'index': 'draconic',
             'name': 'Draconic',
             'url': '/api/languages/draconic'},
         {
             'index': 'dwarvish',
             'name': 'Dwarvish',
             'url': '/api/languages/dwarvish'},
         {
             'index': 'elvish',
             'name': 'Elvish',
             'url': '/api/languages/elvish'},
         {
             'index': 'giant',
             'name': 'Giant',
             'url': '/api/languages/giant'},
         {
             'index': 'gnomish',
             'name': 'Gnomish',
             'url': '/api/languages/gnomish'},
         {
             'index': 'goblin',
             'name': 'Goblin',
             'url': '/api/languages/goblin'},
         {
             'index': 'halfling',
             'name': 'Halfling',
             'url': '/api/languages/halfling'},
         {
             'index': 'infernal',
             'name': 'Infernal',
             'url': '/api/languages/infernal'},
         {
             'index': 'orc',
             'name': 'Orc',
             'url': '/api/languages/orc'},
         {
             'index': 'primordial',
             'name': 'Primordial',
             'url': '/api/languages/primordial'},
         {
             'index': 'sylvan',
             'name': 'Sylvan',
             'url': '/api/languages/sylvan'},
         {
             'index': 'undercommon',
             'name': 'Undercommon',
             'url': '/api/languages/undercommon'}]}
MAGIC_ITEMS_RESPONSE: Dict[str, Union[int, List[Dict[str, str]]]
] = {'count': 362, 'results': [
    {"index": "adamantine-armor",
     "name": "Adamantine Armor",
     "url": "/api/magic-items/adamantine-armor"}]}
MAGIC_SCHOOLS_RESPONSE: Dict[str, Union[int, List[Union[
    Dict[str, str], Dict[str, str], Dict[str, str],
    Dict[str, str], Dict[str, str], Dict[str, str],
    Dict[str, str], Dict[str, str]]]]
] = {'count': 8,
     'results': [{'index': 'abjuration',
                  'name': 'Abjuration',
                  'url': '/api/magic-schools/abjuration'},
                 {'index': 'conjuration',
                  'name': 'Conjuration',
                  'url': '/api/magic-schools/conjuration'},
                 {'index': 'divination',
                  'name': 'Divination',
                  'url': '/api/magic-schools/divination'},
                 {'index': 'enchantment',
                  'name': 'Enchantment',
                  'url': '/api/magic-schools/enchantment'},
                 {'index': 'evocation',
                  'name': 'Evocation',
                  'url': '/api/magic-schools/evocation'},
                 {'index': 'illusion',
                  'name': 'Illusion',
                  'url': '/api/magic-schools/illusion'},
                 {'index': 'necromancy',
                  'name': 'Necromancy',
                  'url': '/api/magic-schools/necromancy'},
                 {'index': 'transmutation',
                  'name': 'Transmutation',
                  'url': '/api/magic-schools/transmutation'}]}
MONSTERS_RESPONSE: Dict[str, Union[int, List[Dict[str, str]]]
] = {
    'count': 334,
    'results': [{
        "index": "aboleth",
        "name": "Aboleth",
        "url": "/api/monsters/aboleth"
    }]}
PROFICIENCIES_RESPONSE: Dict[str, Union[int, List[Dict[str, str]]]
] = {'count': 117, 'results': [
    {"index": "alchemists-supplies",
     "name": "Alchemist's Supplies",
     "url": "/api/proficiencies/alchemists-supplies"}
]}
RACES_RESPONSE: Dict[str, Union[int, List[Union[
    Dict[str, str], Dict[str, str], Dict[str, str],
    Dict[str, str], Dict[str, str], Dict[str, str],
    Dict[str, str], Dict[str, str], Dict[str, str]]]]
] = {'count': 9,
     'results': [{'index': 'dragonborn',
                  'name': 'Dragonborn',
                  'url': '/api/races/dragonborn'},
                 {'index': 'dwarf', 'name': 'Dwarf',
                  'url': '/api/races/dwarf'},
                 {'index': 'elf', 'name': 'Elf',
                  'url': '/api/races/elf'},
                 {'index': 'gnome', 'name': 'Gnome',
                  'url': '/api/races/gnome'},
                 {'index': 'half-elf',
                  'name': 'Half-Elf',
                  'url': '/api/races/half-elf'},
                 {'index': 'half-orc',
                  'name': 'Half-Orc',
                  'url': '/api/races/half-orc'},
                 {'index': 'halfling',
                  'name': 'Halfling',
                  'url': '/api/races/halfling'},
                 {'index': 'human', 'name': 'Human',
                  'url': '/api/races/human'},
                 {'index': 'tiefling',
                  'name': 'Tiefling',
                  'url': '/api/races/tiefling'}]}
RULE_SECTIONS_RESPONSE: Dict[str, Union[int, List[
    Union[Union[Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str]], Any]]]
] = {'count': 33,
     'results': [
         {'index': 'ability-checks',
          'name': 'Ability Checks',
          'url': '/api/rule-sections/ability-checks'},
         {
             'index': 'ability-scores-and-modifiers',
             'name': 'Ability Scores and Modifiers',
             'url': '/api/rule-sections/ability-scores-and-modifiers'},
         {
             'index': 'actions-in-combat',
             'name': 'Actions in Combat',
             'url': '/api/rule-sections/actions-in-combat'},
         {
             'index': 'activating-an-item',
             'name': 'Activating an Item',
             'url': '/api/rule-sections/activating-an-item'},
         {
             'index': 'advantage-and-disadvantage',
             'name': 'Advantage and Disadvantage',
             'url': '/api/rule-sections/advantage-and-disadvantage'},
         {'index': 'attunement',
          'name': 'Attunement',
          'url': '/api/rule-sections/attunement'},
         {
             'index': 'between-adventures',
             'name': 'Between Adventures',
             'url': '/api/rule-sections/between-adventures'},
         {
             'index': 'casting-a-spell',
             'name': 'Casting a Spell',
             'url': '/api/rule-sections/casting-a-spell'},
         {'index': 'cover',
          'name': 'Cover',
          'url': '/api/rule-sections/cover'},
         {
             'index': 'damage-and-healing',
             'name': 'Damage and Healing',
             'url': '/api/rule-sections/damage-and-healing'},
         {'index': 'diseases',
          'name': 'Diseases',
          'url': '/api/rule-sections/diseases'},
         {
             'index': 'fantasy-historical-pantheons',
             'name': 'Fantasy-Historical Pantheons',
             'url': '/api/rule-sections/fantasy-historical-pantheons'},
         {'index': 'madness',
          'name': 'Madness',
          'url': '/api/rule-sections/madness'},
         {
             'index': 'making-an-attack',
             'name': 'Making an Attack',
             'url': '/api/rule-sections/making-an-attack'},
         {'index': 'mounted-combat',
          'name': 'Mounted Combat',
          'url': '/api/rule-sections/mounted-combat'},
         {'index': 'movement',
          'name': 'Movement',
          'url': '/api/rule-sections/movement'},
         {
             'index': 'movement-and-position',
             'name': 'Movement and Position',
             'url': '/api/rule-sections/movement-and-position'},
         {'index': 'objects',
          'name': 'Objects',
          'url': '/api/rule-sections/objects'},
         {'index': 'poisons',
          'name': 'Poisons',
          'url': '/api/rule-sections/poisons'},
         {
             'index': 'proficiency-bonus',
             'name': 'Proficiency Bonus',
             'url': '/api/rule-sections/proficiency-bonus'},
         {'index': 'resting',
          'name': 'Resting',
          'url': '/api/rule-sections/resting'},
         {'index': 'saving-throws',
          'name': 'Saving Throws',
          'url': '/api/rule-sections/saving-throws'},
         {
             'index': 'sentient-magic-items',
             'name': 'Sentient Magic Items',
             'url': '/api/rule-sections/sentient-magic-items'},
         {
             'index': 'standard-exchange-rates',
             'name': 'Standard Exchange Rates',
             'url': '/api/rule-sections/standard-exchange-rates'},
         {
             'index': 'the-environment',
             'name': 'The Environment',
             'url': '/api/rule-sections/the-environment'},
         {
             'index': 'the-order-of-combat',
             'name': 'The Order of Combat',
             'url': '/api/rule-sections/the-order-of-combat'},
         {
             'index': 'the-planes-of-existence',
             'name': 'The Planes of Existence',
             'url': '/api/rule-sections/the-planes-of-existence'},
         {'index': 'time',
          'name': 'Time',
          'url': '/api/rule-sections/time'},
         {'index': 'traps',
          'name': 'Traps',
          'url': '/api/rule-sections/traps'},
         {
             'index': 'underwater-combat',
             'name': 'Underwater Combat',
             'url': '/api/rule-sections/underwater-combat'},
         {
             'index': 'using-each-ability',
             'name': 'Using Each Ability',
             'url': '/api/rule-sections/using-each-ability'},
         {
             'index': 'wearing-and-wielding-items',
             'name': 'Wearing and Wielding Items',
             'url': '/api/rule-sections/wearing-and-wielding-items'},
         {
             'index': 'what-is-a-spell',
             'name': 'What Is a Spell?',
             'url': '/api/rule-sections/what-is-a-spell'}]}
RULES_RESPONSE: Dict[str, Union[int, List[
    Union[Dict[str, str], Dict[str, str], Dict[str, str],
          Dict[str, str], Dict[str, str], Dict[str, str]]]]] = {
    'count': 6,
    'results': [{'index': 'adventuring',
                 'name': 'Adventuring',
                 'url': '/api/rules/adventuring'},
                {'index': 'appendix',
                 'name': 'Appendix',
                 'url': '/api/rules/appendix'},
                {'index': 'combat', 'name': 'Combat', 'url': '/api/rules/combat'},
                {'index': 'equipment',
                 'name': 'Equipment',
                 'url': '/api/rules/equipment'},
                {'index': 'spellcasting',
                 'name': 'Spellcasting',
                 'url': '/api/rules/spellcasting'},
                {'index': 'using-ability-scores',
                 'name': 'Using Ability Scores',
                 'url': '/api/rules/using-ability-scores'}]}
SKILLS_RESPONSE: Dict[str, Union[int, List[
    Union[Union[Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str]], Any]]]
] = {'count': 18,
     'results': [{
         'index': 'acrobatics',
         'name': 'Acrobatics',
         'url': '/api/skills/acrobatics'},
         {
             'index': 'animal-handling',
             'name': 'Animal Handling',
             'url': '/api/skills/animal-handling'},
         {
             'index': 'arcana',
             'name': 'Arcana',
             'url': '/api/skills/arcana'},
         {
             'index': 'athletics',
             'name': 'Athletics',
             'url': '/api/skills/athletics'},
         {
             'index': 'deception',
             'name': 'Deception',
             'url': '/api/skills/deception'},
         {
             'index': 'history',
             'name': 'History',
             'url': '/api/skills/history'},
         {
             'index': 'insight',
             'name': 'Insight',
             'url': '/api/skills/insight'},
         {
             'index': 'intimidation',
             'name': 'Intimidation',
             'url': '/api/skills/intimidation'},
         {
             'index': 'investigation',
             'name': 'Investigation',
             'url': '/api/skills/investigation'},
         {
             'index': 'medicine',
             'name': 'Medicine',
             'url': '/api/skills/medicine'},
         {
             'index': 'nature',
             'name': 'Nature',
             'url': '/api/skills/nature'},
         {
             'index': 'perception',
             'name': 'Perception',
             'url': '/api/skills/perception'},
         {
             'index': 'performance',
             'name': 'Performance',
             'url': '/api/skills/performance'},
         {
             'index': 'persuasion',
             'name': 'Persuasion',
             'url': '/api/skills/persuasion'},
         {
             'index': 'religion',
             'name': 'Religion',
             'url': '/api/skills/religion'},
         {
             'index': 'sleight-of-hand',
             'name': 'Sleight of Hand',
             'url': '/api/skills/sleight-of-hand'},
         {
             'index': 'stealth',
             'name': 'Stealth',
             'url': '/api/skills/stealth'},
         {
             'index': 'survival',
             'name': 'Survival',
             'url': '/api/skills/survival'}]}
SPELLS_RESPONSE: Dict[str, Union[int, List[Dict[str, str]]]
] = {'count': 319,
     'results': [
         {"index": "acid-arrow", "name": "Acid Arrow",
          "url": "/api/spells/acid-arrow"}]}
SUBCLASSES_RESPONSE: Dict[str, Union[int, List[
    Union[Union[Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str]], Any]]]
] = {'count': 12,
     'results': [{
         'index': 'berserker',
         'name': 'Berserker',
         'url': '/api/subclasses/berserker'},
         {
             'index': 'champion',
             'name': 'Champion',
             'url': '/api/subclasses/champion'},
         {
             'index': 'devotion',
             'name': 'Devotion',
             'url': '/api/subclasses/devotion'},
         {
             'index': 'draconic',
             'name': 'Draconic',
             'url': '/api/subclasses/draconic'},
         {
             'index': 'evocation',
             'name': 'Evocation',
             'url': '/api/subclasses/evocation'},
         {
             'index': 'fiend',
             'name': 'Fiend',
             'url': '/api/subclasses/fiend'},
         {
             'index': 'hunter',
             'name': 'Hunter',
             'url': '/api/subclasses/hunter'},
         {
             'index': 'land',
             'name': 'Land',
             'url': '/api/subclasses/land'},
         {
             'index': 'life',
             'name': 'Life',
             'url': '/api/subclasses/life'},
         {
             'index': 'lore',
             'name': 'Lore',
             'url': '/api/subclasses/lore'},
         {
             'index': 'open-hand',
             'name': 'Open Hand',
             'url': '/api/subclasses/open-hand'},
         {
             'index': 'thief',
             'name': 'Thief',
             'url': '/api/subclasses/thief'}]}
SUBRACES_RESPONSE: Dict[
    str, Union[int, List[Union[
        Dict[str, str], Dict[str, str],
        Dict[str, str], Dict[str, str]]]]
] = {'count': 4,
     'results': [{
         'index': 'high-elf',
         'name': 'High Elf',
         'url': '/api/subraces/high-elf'},
         {
             'index': 'hill-dwarf',
             'name': 'Hill Dwarf',
             'url': '/api/subraces/hill-dwarf'},
         {
             'index': 'lightfoot-halfling',
             'name': 'Lightfoot Halfling',
             'url': '/api/subraces/lightfoot-halfling'},
         {
             'index': 'rock-gnome',
             'name': 'Rock Gnome',
             'url': '/api/subraces/rock-gnome'}]}
TRAITS_RESPONSE: Dict[str, Union[int, List[
    Union[Union[Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str]], Any]]]
] = {'count': 38,
     'results': [{
         'index': 'artificers-lore',
         'name': "Artificer's Lore",
         'url': '/api/traits/artificers-lore'},
         {
             'index': 'brave',
             'name': 'Brave',
             'url': '/api/traits/brave'},
         {
             'index': 'breath-weapon',
             'name': 'Breath Weapon',
             'url': '/api/traits/breath-weapon'},
         {
             'index': 'damage-resistance',
             'name': 'Damage Resistance',
             'url': '/api/traits/damage-resistance'},
         {
             'index': 'darkvision',
             'name': 'Darkvision',
             'url': '/api/traits/darkvision'},
         {
             'index': 'draconic-ancestry',
             'name': 'Draconic Ancestry',
             'url': '/api/traits/draconic-ancestry'},
         {
             'index': 'draconic-ancestry-black',
             'name': 'Draconic Ancestry (Black)',
             'url': '/api/traits/draconic-ancestry-black'},
         {
             'index': 'draconic-ancestry-blue',
             'name': 'Draconic Ancestry (Blue)',
             'url': '/api/traits/draconic-ancestry-blue'},
         {
             'index': 'draconic-ancestry-brass',
             'name': 'Draconic Ancestry (Brass)',
             'url': '/api/traits/draconic-ancestry-brass'},
         {
             'index': 'draconic-ancestry-bronze',
             'name': 'Draconic Ancestry (Bronze)',
             'url': '/api/traits/draconic-ancestry-bronze'},
         {
             'index': 'draconic-ancestry-copper',
             'name': 'Draconic Ancestry (Copper)',
             'url': '/api/traits/draconic-ancestry-copper'},
         {
             'index': 'draconic-ancestry-gold',
             'name': 'Draconic Ancestry (Gold)',
             'url': '/api/traits/draconic-ancestry-gold'},
         {
             'index': 'draconic-ancestry-green',
             'name': 'Draconic Ancestry (Green)',
             'url': '/api/traits/draconic-ancestry-green'},
         {
             'index': 'draconic-ancestry-red',
             'name': 'Draconic Ancestry (Red)',
             'url': '/api/traits/draconic-ancestry-red'},
         {
             'index': 'draconic-ancestry-silver',
             'name': 'Draconic Ancestry (Silver)',
             'url': '/api/traits/draconic-ancestry-silver'},
         {
             'index': 'draconic-ancestry-white',
             'name': 'Draconic Ancestry (White)',
             'url': '/api/traits/draconic-ancestry-white'},
         {
             'index': 'dwarven-combat-training',
             'name': 'Dwarven Combat Training',
             'url': '/api/traits/dwarven-combat-training'},
         {
             'index': 'dwarven-resilience',
             'name': 'Dwarven Resilience',
             'url': '/api/traits/dwarven-resilience'},
         {
             'index': 'dwarven-toughness',
             'name': 'Dwarven Toughness',
             'url': '/api/traits/dwarven-toughness'},
         {
             'index': 'elf-weapon-training',
             'name': 'Elf Weapon Training',
             'url': '/api/traits/elf-weapon-training'},
         {
             'index': 'extra-language',
             'name': 'Extra Language',
             'url': '/api/traits/extra-language'},
         {
             'index': 'fey-ancestry',
             'name': 'Fey Ancestry',
             'url': '/api/traits/fey-ancestry'},
         {
             'index': 'gnome-cunning',
             'name': 'Gnome Cunning',
             'url': '/api/traits/gnome-cunning'},
         {
             'index': 'halfling-nimbleness',
             'name': 'Halfling Nimbleness',
             'url': '/api/traits/halfling-nimbleness'},
         {
             'index': 'hellish-resistance',
             'name': 'Hellish Resistance',
             'url': '/api/traits/hellish-resistance'},
         {
             'index': 'high-elf-cantrip',
             'name': 'High Elf Cantrip',
             'url': '/api/traits/high-elf-cantrip'},
         {
             'index': 'infernal-legacy',
             'name': 'Infernal Legacy',
             'url': '/api/traits/infernal-legacy'},
         {
             'index': 'keen-senses',
             'name': 'Keen Senses',
             'url': '/api/traits/keen-senses'},
         {
             'index': 'lucky',
             'name': 'Lucky',
             'url': '/api/traits/lucky'},
         {
             'index': 'menacing',
             'name': 'Menacing',
             'url': '/api/traits/menacing'},
         {
             'index': 'naturally-stealthy',
             'name': 'Naturally Stealthy',
             'url': '/api/traits/naturally-stealthy'},
         {
             'index': 'relentless-endurance',
             'name': 'Relentless Endurance',
             'url': '/api/traits/relentless-endurance'},
         {
             'index': 'savage-attacks',
             'name': 'Savage Attacks',
             'url': '/api/traits/savage-attacks'},
         {
             'index': 'skill-versatility',
             'name': 'Skill Versatility',
             'url': '/api/traits/skill-versatility'},
         {
             'index': 'stonecunning',
             'name': 'Stonecunning',
             'url': '/api/traits/stonecunning'},
         {
             'index': 'tinker',
             'name': 'Tinker',
             'url': '/api/traits/tinker'},
         {
             'index': 'tool-proficiency',
             'name': 'Tool Proficiency',
             'url': '/api/traits/tool-proficiency'},
         {
             'index': 'trance',
             'name': 'Trance',
             'url': '/api/traits/trance'}]}
WEAPON_PROPERTIES_RESPONSE: Dict[str, Union[int, List[
    Union[Union[Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str], Dict[str, str], Dict[str, str],
                Dict[str, str]], Any]]]
] = {'count': 11,
     'results': [
         {'index': 'ammunition',
          'name': 'Ammunition',
          'url': '/api/weapon-properties/ammunition'},
         {'index': 'finesse',
          'name': 'Finesse',
          'url': '/api/weapon-properties/finesse'},
         {'index': 'heavy',
          'name': 'Heavy',
          'url': '/api/weapon-properties/heavy'},
         {'index': 'light',
          'name': 'Light',
          'url': '/api/weapon-properties/light'},
         {'index': 'loading',
          'name': 'Loading',
          'url': '/api/weapon-properties/loading'},
         {'index': 'monk',
          'name': 'Monk',
          'url': '/api/weapon-properties/monk'},
         {'index': 'reach',
          'name': 'Reach',
          'url': '/api/weapon-properties/reach'},
         {'index': 'special',
          'name': 'Special',
          'url': '/api/weapon-properties/special'},
         {'index': 'thrown',
          'name': 'Thrown',
          'url': '/api/weapon-properties/thrown'},
         {'index': 'two-handed',
          'name': 'Two-Handed',
          'url': '/api/weapon-properties/two-handed'},
         {'index': 'versatile',
          'name': 'Versatile',
          'url': '/api/weapon-properties/versatile'}]}
_RESPONSE: None = None


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
        result_json: Union[Dict[str, object], Any] = self.dnd.__get_json__()
        self.assertEqual(GOOD_BASE_RESPONSE, result_json)
        bad_result: Union[Dict[str, object], Any] = self.bad_dnd.__get_json__()
        self.assertEqual(BAD_404_RESPONSE, bad_result)

    def test__get_df__(self) -> None:
        """

        Returns
        -------

        """
        result_df: DataFrame = self.dnd.__get_df__()
        self.assertEqual("/api/ability-scores", result_df.at["ability-scores", "url"])
        bad_result_df: DataFrame = self.bad_dnd.__get_df__()
        self.assertEqual(404, bad_result_df.at[0, "status_code"])

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd.url_root)
        self.assertEqual("/api", self.dnd.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api", self.dnd.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd.requests_args["headers"])
        self.assertIsInstance(self.dnd.dframe, pd.DataFrame)
        self.assertEqual((24, 2), self.dnd.dframe.shape)
        self.assertEqual(URL_ROOT, self.bad_dnd.url_root)
        self.assertEqual("/api/Bad_Leaf_69_420", self.bad_dnd.url_leaf)
        self.assertEqual(
            "https://www.dnd5eapi.co/api/Bad_Leaf_69_420", self.bad_dnd.requests_args["url"]
        )
        self.assertEqual(HEADERS, self.bad_dnd.requests_args["headers"])
        self.assertIsInstance(self.bad_dnd.dframe, pd.DataFrame)
        self.assertEqual((1, 1), self.bad_dnd.dframe.shape)

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
        self.assertIn("obj", self.dnd.dframe.columns)
        self.dnd.dframe["obj"].apply(lambda x: self.assertIsInstance(x, self.constructor))
        self.assertWarns(ResourceWarning, self.bad_dnd.create_instances_from_urls)


class TestGetLeafConstructorMap(TestCase):
    """

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
        [self.assertIsInstance(obj, self.constructor) for obj in called]


class TestAbilityScores(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_ability_scores = dnd5eapy.AbilityScores(url_root=URL_ROOT)

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_ability_scores.url_root)
        self.assertEqual("/api/ability-scores", self.dnd_ability_scores.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/ability-scores", self.dnd_ability_scores.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_ability_scores.requests_args["headers"])
        self.assertIsInstance(self.dnd_ability_scores.dframe, pd.DataFrame)
        self.assertEqual((6, 2), self.dnd_ability_scores.dframe.shape)

    def test_create_instances_from_urls(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_ability_scores.create_instances_from_urls()


class TestAbilityScore(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_ability_score = dnd5eapy.abilityscores.AbilityScore()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_ability_score.url_root)
        self.assertEqual("/api/ability-scores/cha", self.dnd_ability_score.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/ability-scores/cha", self.dnd_ability_score.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_ability_score.requests_args["headers"])
        self.assertIsInstance(self.dnd_ability_score.dframe, pd.DataFrame)
        self.assertEqual((1, 5), self.dnd_ability_score.dframe.shape)


class TestAlignments(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_alignments = dnd5eapy.alignments.Alignments()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_alignments.url_root)
        self.assertEqual("/api/alignments", self.dnd_alignments.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/alignments", self.dnd_alignments.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_alignments.requests_args["headers"])
        self.assertIsInstance(self.dnd_alignments.dframe, pd.DataFrame)
        self.assertEqual((9, 2), self.dnd_alignments.dframe.shape)


class TestBackgrounds(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_backgrounds = dnd5eapy.backgrounds.Backgrounds()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_backgrounds.url_root)
        self.assertEqual("/api/backgrounds", self.dnd_backgrounds.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/backgrounds", self.dnd_backgrounds.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_backgrounds.requests_args["headers"])
        self.assertIsInstance(self.dnd_backgrounds.dframe, pd.DataFrame)
        self.assertEqual((1, 2), self.dnd_backgrounds.dframe.shape)


class TestClasses(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_classes = dnd5eapy.classes.Classes()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_classes.url_root)
        self.assertEqual("/api/classes", self.dnd_classes.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/classes", self.dnd_classes.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_classes.requests_args["headers"])
        self.assertIsInstance(self.dnd_classes.dframe, pd.DataFrame)
        self.assertEqual((12, 2), self.dnd_classes.dframe.shape)


class TestConditions(TestCase):
    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_conditions = dnd5eapy.conditions.Conditions()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_conditions.url_root)
        self.assertEqual("/api/conditions", self.dnd_conditions.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/conditions", self.dnd_conditions.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_conditions.requests_args["headers"])
        self.assertIsInstance(self.dnd_conditions.dframe, pd.DataFrame)
        self.assertEqual((15, 2), self.dnd_conditions.dframe.shape)


class TestDamageTypes(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_damage_types = dnd5eapy.damagetypes.DamageTypes()

    def test_attributes(self) -> None:
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_damage_types.url_root)
        self.assertEqual("/api/damage-types", self.dnd_damage_types.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/damage-types", self.dnd_damage_types.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_damage_types.requests_args["headers"])
        self.assertIsInstance(self.dnd_damage_types.dframe, pd.DataFrame)
        self.assertEqual((13, 2), self.dnd_damage_types.dframe.shape)


class TestEquipment(TestCase):
    """

    """
    dnd_equipment: dnd5eapy.equipment.Equipment

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_equipment = dnd5eapy.equipment.Equipment()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_equipment.url_root)
        self.assertEqual("/api/equipment", self.dnd_equipment.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/equipment", self.dnd_equipment.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_equipment.requests_args["headers"])
        self.assertIsInstance(self.dnd_equipment.dframe, pd.DataFrame)
        self.assertEqual((237, 2), self.dnd_equipment.dframe.shape)


class TestEquipmentCategories(TestCase):
    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_equipment_categories = dnd5eapy.equipmentcategories.EquipmentCategories()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_equipment_categories.url_root)
        self.assertEqual("/api/equipment-categories", self.dnd_equipment_categories.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/equipment-categories",
                         self.dnd_equipment_categories.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_equipment_categories.requests_args["headers"])
        self.assertIsInstance(self.dnd_equipment_categories.dframe, pd.DataFrame)
        self.assertEqual((39, 2), self.dnd_equipment_categories.dframe.shape)


class TestFeats(TestCase):
    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_feats = dnd5eapy.feats.Feats()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_feats.url_root)
        self.assertEqual("/api/feats", self.dnd_feats.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/feats", self.dnd_feats.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_feats.requests_args["headers"])
        self.assertIsInstance(self.dnd_feats.dframe, pd.DataFrame)
        self.assertEqual((1, 2), self.dnd_feats.dframe.shape)


class TestFeatures(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_features = dnd5eapy.features.Features()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_features.url_root)
        self.assertEqual("/api/features", self.dnd_features.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/features", self.dnd_features.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_features.requests_args["headers"])
        self.assertIsInstance(self.dnd_features.dframe, pd.DataFrame)
        self.assertEqual((370, 2), self.dnd_features.dframe.shape)


class TestLanguages(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_languages = dnd5eapy.languages.Languages()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_languages.url_root)
        self.assertEqual("/api/languages", self.dnd_languages.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/languages", self.dnd_languages.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_languages.requests_args["headers"])
        self.assertIsInstance(self.dnd_languages.dframe, pd.DataFrame)
        self.assertEqual((16, 2), self.dnd_languages.dframe.shape)


class TestMagicItems(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_magic_items = dnd5eapy.magicitems.MagicItems()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_magic_items.url_root)
        self.assertEqual("/api/magic-items", self.dnd_magic_items.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/magic-items", self.dnd_magic_items.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_magic_items.requests_args["headers"])
        self.assertIsInstance(self.dnd_magic_items.dframe, pd.DataFrame)
        self.assertEqual((362, 2), self.dnd_magic_items.dframe.shape)


class TestMagicSchools(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_magic_schools = dnd5eapy.magicschools.MagicSchools()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_magic_schools.url_root)
        self.assertEqual("/api/magic-schools", self.dnd_magic_schools.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/magic-schools", self.dnd_magic_schools.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_magic_schools.requests_args["headers"])
        self.assertIsInstance(self.dnd_magic_schools.dframe, pd.DataFrame)
        self.assertEqual((8, 2), self.dnd_magic_schools.dframe.shape)


class TestMonsters(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_monsters = dnd5eapy.monsters.Monsters()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_monsters.url_root)
        self.assertEqual("/api/monsters", self.dnd_monsters.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/monsters", self.dnd_monsters.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_monsters.requests_args["headers"])
        self.assertIsInstance(self.dnd_monsters.dframe, pd.DataFrame)
        self.assertEqual((334, 2), self.dnd_monsters.dframe.shape)


class TestProficiencies(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_proficiencies = dnd5eapy.proficiencies.Proficiencies()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_proficiencies.url_root)
        self.assertEqual("/api/proficiencies", self.dnd_proficiencies.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/proficiencies", self.dnd_proficiencies.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_proficiencies.requests_args["headers"])
        self.assertIsInstance(self.dnd_proficiencies.dframe, pd.DataFrame)
        self.assertEqual((117, 2), self.dnd_proficiencies.dframe.shape)


class TestRaces(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_races = dnd5eapy.races.Races()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_races.url_root)
        self.assertEqual("/api/races", self.dnd_races.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/races", self.dnd_races.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_races.requests_args["headers"])
        self.assertIsInstance(self.dnd_races.dframe, pd.DataFrame)
        self.assertEqual((9, 2), self.dnd_races.dframe.shape)


class TestRuleSections(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_rule_sections = dnd5eapy.rulesections.RuleSections()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_rule_sections.url_root)
        self.assertEqual("/api/rule-sections", self.dnd_rule_sections.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/rule-sections", self.dnd_rule_sections.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_rule_sections.requests_args["headers"])
        self.assertIsInstance(self.dnd_rule_sections.dframe, pd.DataFrame)
        self.assertEqual((33, 2), self.dnd_rule_sections.dframe.shape)


class TestRules(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_rules = dnd5eapy.rules.Rules()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_rules.url_root)
        self.assertEqual("/api/rules", self.dnd_rules.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/rules", self.dnd_rules.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_rules.requests_args["headers"])
        self.assertIsInstance(self.dnd_rules.dframe, pd.DataFrame)
        self.assertEqual((6, 2), self.dnd_rules.dframe.shape)


class TestSkills(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_skills = dnd5eapy.skills.Skills()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_skills.url_root)
        self.assertEqual("/api/skills", self.dnd_skills.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/skills", self.dnd_skills.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_skills.requests_args["headers"])
        self.assertIsInstance(self.dnd_skills.dframe, pd.DataFrame)
        self.assertEqual((18, 2), self.dnd_skills.dframe.shape)


class TestSpells(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_spells = dnd5eapy.spells.Spells()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_spells.url_root)
        self.assertEqual("/api/spells", self.dnd_spells.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/spells", self.dnd_spells.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_spells.requests_args["headers"])
        self.assertIsInstance(self.dnd_spells.dframe, pd.DataFrame)
        self.assertEqual((319, 2), self.dnd_spells.dframe.shape)


class TestSubclasses(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_subclasses = dnd5eapy.subclasses.Subclasses()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_subclasses.url_root)
        self.assertEqual("/api/subclasses", self.dnd_subclasses.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/subclasses", self.dnd_subclasses.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_subclasses.requests_args["headers"])
        self.assertIsInstance(self.dnd_subclasses.dframe, pd.DataFrame)
        self.assertEqual((12, 2), self.dnd_subclasses.dframe.shape)


class TestSubraces(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_subraces = dnd5eapy.subraces.Subraces()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_subraces.url_root)
        self.assertEqual("/api/subraces", self.dnd_subraces.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/subraces", self.dnd_subraces.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_subraces.requests_args["headers"])
        self.assertIsInstance(self.dnd_subraces.dframe, pd.DataFrame)
        self.assertEqual((4, 2), self.dnd_subraces.dframe.shape)


class TestTraits(TestCase):
    """

    """

    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_traits = dnd5eapy.traits.Traits()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual(URL_ROOT, self.dnd_traits.url_root)
        self.assertEqual("/api/traits", self.dnd_traits.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/traits", self.dnd_traits.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_traits.requests_args["headers"])
        self.assertIsInstance(self.dnd_traits.dframe, pd.DataFrame)
        self.assertEqual((38, 2), self.dnd_traits.dframe.shape)


class TestWeaponProperties(TestCase):
    """

    """
    def setUp(self) -> None:
        """

        Returns
        -------

        """
        self.dnd_weapon_properties = dnd5eapy.weaponproperties.WeaponProperties()

    def test_attributes(self):
        """

        Returns
        -------

        """
        self.assertEqual("https://www.dnd5eapi.co", self.dnd_weapon_properties.url_root)
        self.assertEqual("/api/weapon-properties", self.dnd_weapon_properties.url_leaf)
        self.assertEqual("https://www.dnd5eapi.co/api/weapon-properties",
                         self.dnd_weapon_properties.requests_args["url"])
        self.assertEqual(HEADERS, self.dnd_weapon_properties.requests_args["headers"])
        self.assertIsInstance(self.dnd_weapon_properties.dframe, pd.DataFrame)
        self.assertEqual((11, 2), self.dnd_weapon_properties.dframe.shape)
