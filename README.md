[![Python package](
https://github.com/Phillyclause89/DnD5eAPIBrowser/actions/workflows/python-package.yml/badge.svg?branch=main
)](https://github.com/Phillyclause89/DnD5eAPIBrowser/actions/workflows/python-package.yml)

# [DnD5eAPIBrowser](https://github.com/Phillyclause89/DnD5eAPIBrowser)

Under development python library for working with https://www.dnd5eapi.co/api responses in python.

#### Notes:

- [dnd5eapy](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy) is the lib under development here.
- Everything else in the top level of this repro is for testing the lib.

    - [test_dnd5eapy.py](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/test_dnd5eapy.py) are the unit
      tests for the lib
    - [main.py](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/main.py) is as shitty tkinter app used to
      manually test the lib.

## [dnd5eapy](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy)

The bread and butter of [dnd5eapy](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy) is
the [DnD5eAPIObj](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy/core/__init__.py#L50) class.
This is the base parent class for all other classes in the lib as well as user level class for working with data
returned by the [root api endpoint](https://www.dnd5eapi.co/api):

```json
{
  "ability-scores": "/api/ability-scores",
  "alignments": "/api/alignments",
  "backgrounds": "/api/backgrounds",
  "classes": "/api/classes",
  "conditions": "/api/conditions",
  "damage-types": "/api/damage-types",
  "equipment": "/api/equipment",
  "equipment-categories": "/api/equipment-categories",
  "feats": "/api/feats",
  "features": "/api/features",
  "languages": "/api/languages",
  "magic-items": "/api/magic-items",
  "magic-schools": "/api/magic-schools",
  "monsters": "/api/monsters",
  "proficiencies": "/api/proficiencies",
  "races": "/api/races",
  "rule-sections": "/api/rule-sections",
  "rules": "/api/rules",
  "skills": "/api/skills",
  "spells": "/api/spells",
  "subclasses": "/api/subclasses",
  "subraces": "/api/subraces",
  "traits": "/api/traits",
  "weapon-properties": "/api/weapon-properties"
}
```

When a [DnD5eAPIObj](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy/core/__init__.py#L50) object
is initialized, it will create and store
a [pandas.DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) representation of the response
data:

````pycon
>>> import dnd5eapy
>>> dnd = dnd5eapy.DnD5eAPIObj()
>>> print(dnd)
<dnd5eapy.core.DnD5eAPIObj object from https://www.dnd5eapi.co/api at 0x0000022FB90E0E10>
>>> print(dnd.df)
                                      name                        url
index                                                                
ability-scores              Ability Scores        /api/ability-scores
alignments                      Alignments            /api/alignments
backgrounds                    Backgrounds           /api/backgrounds
classes                            Classes               /api/classes
conditions                      Conditions            /api/conditions
damage-types                  Damage Types          /api/damage-types
equipment                        Equipment             /api/equipment
equipment-categories  Equipment Categories  /api/equipment-categories
feats                                Feats                 /api/feats
features                          Features              /api/features
languages                        Languages             /api/languages
magic-items                    Magic Items           /api/magic-items
magic-schools                Magic Schools         /api/magic-schools
monsters                          Monsters              /api/monsters
proficiencies                Proficiencies         /api/proficiencies
races                                Races                 /api/races
rule-sections                Rule Sections         /api/rule-sections
rules                                Rules                 /api/rules
skills                              Skills                /api/skills
spells                              Spells                /api/spells
subclasses                      Subclasses            /api/subclasses
subraces                          Subraces              /api/subraces
traits                              Traits                /api/traits
weapon-properties        Weapon Properties     /api/weapon-properties
>>> 
````

The [DnD5eAPIObj](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy/core/__init__.py#L50) object is
not a child of any pandas object. But it does offer direct access to several commony used members of the df (including
some magic methods):

```pycon
>>> print(dnd.columns)
Index(['name', 'url'], dtype='object')
>>> print(dnd.index)
Index(['ability-scores', 'alignments', 'backgrounds', 'classes', 'conditions',
       'damage-types', 'equipment', 'equipment-categories', 'feats',
       'features', 'languages', 'magic-items', 'magic-schools', 'monsters',
       'proficiencies', 'races', 'rule-sections', 'rules', 'skills', 'spells',
       'subclasses', 'subraces', 'traits', 'weapon-properties'],
      dtype='object', name='index')
>>> print(dnd['url'] == dnd.url_column)
index
ability-scores          True
alignments              True
backgrounds             True
classes                 True
conditions              True
damage-types            True
equipment               True
equipment-categories    True
feats                   True
features                True
languages               True
magic-items             True
magic-schools           True
monsters                True
proficiencies           True
races                   True
rule-sections           True
rules                   True
skills                  True
spells                  True
subclasses              True
subraces                True
traits                  True
weapon-properties       True
Name: url, dtype: bool
>>> 
```

Each child class of
the [DnD5eAPIObj](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy/core/__init__.py#L50) object
is designed for working specifically with the data returned by its associated url_leaf. You can get a map of these
`url_leaf`'s to their appropriate class constructors by calling
[get_leaf_constructor_map](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy/core/__init__.py#L721):

```pycon
>>> print(dnd5eapy.get_leaf_constructor_map())
{'/api': <class 'dnd5eapy.core.DnD5eAPIObj'>, '/api/subraces/*': <class 'dnd5eapy.subraces.Subrace'>, '/api/classes/*': <class 'dnd5eapy.classes.Class'>, '/api/conditions': <class 'dnd5eapy.conditions.Conditions'>, '/api/skills': <class 'dnd5eapy.skills.Skills'>, '/api/traits': <class 'dnd5eapy.traits.Traits'>, '/api/races/*': <class 'dnd5eapy.races.Race'>, '/api/features/*': <class 'dnd5eapy.features.Feature'>, '/api/backgrounds': <class 'dnd5eapy.backgrounds.Backgrounds'>, '/api/proficiencies/*': <class 'dnd5eapy.proficiencies.Proficiency'>, '/api/magic-schools/*': <class 'dnd5eapy.magicschools.MagicSchool'>, '/api/features': <class 'dnd5eapy.features.Features'>, '/api/ability-scores': <class 'dnd5eapy.abilityscores.AbilityScores'>, '/api/monsters': <class 'dnd5eapy.monsters.Monsters'>, '/api/races': <class 'dnd5eapy.races.Races'>, '/api/equipment-categories/*': <class 'dnd5eapy.equipmentcategories.EquipmentCategory'>, '/api/subclasses': <class 'dnd5eapy.subclasses.Subclasses'>, '/api/rule-sections/*': <class 'dnd5eapy.rulesections.RuleSection'>, '/api/equipment-categories': <class 'dnd5eapy.equipmentcategories.EquipmentCategories'>, '/api/weapon-properties/*': <class 'dnd5eapy.weaponproperties.WeaponProperty'>, '/api/rule-sections': <class 'dnd5eapy.rulesections.RuleSections'>, '/api/damage-types': <class 'dnd5eapy.damagetypes.DamageTypes'>, '/api/equipment/*': <class 'dnd5eapy.equipment.EquipmentItem'>, '/api/alignments': <class 'dnd5eapy.alignments.Alignments'>, '/api/magic-items/*': <class 'dnd5eapy.magicitems.MagicItem'>, '/api/languages/*': <class 'dnd5eapy.languages.Language'>, '/api/conditions/*': <class 'dnd5eapy.conditions.Condition'>, '/api/traits/*': <class 'dnd5eapy.traits.Trait'>, '/api/subraces': <class 'dnd5eapy.subraces.Subraces'>, '/api/languages': <class 'dnd5eapy.languages.Languages'>, '/api/backgrounds/*': <class 'dnd5eapy.backgrounds.Background'>, '/api/subclasses/*': <class 'dnd5eapy.subclasses.Subclass'>, '/api/rules': <class 'dnd5eapy.rules.Rules'>, '/api/classes': <class 'dnd5eapy.classes.Classes'>, '/api/ability-scores/*': <class 'dnd5eapy.abilityscores.AbilityScore'>, '/api/proficiencies': <class 'dnd5eapy.proficiencies.Proficiencies'>, '/api/weapon-properties': <class 'dnd5eapy.weaponproperties.WeaponProperties'>, '/api/feats': <class 'dnd5eapy.feats.Feats'>, '/api/skills/*': <class 'dnd5eapy.skills.Skill'>, '/api/rules/*': <class 'dnd5eapy.rules.Rule'>, '/api/monsters/*': <class 'dnd5eapy.monsters.Monster'>, '/api/spells': <class 'dnd5eapy.spells.Spells'>, '/api/alignments/*': <class 'dnd5eapy.alignments.Alignment'>, '/api/magic-items': <class 'dnd5eapy.magicitems.MagicItems'>, '/api/spells/*': <class 'dnd5eapy.spells.Spell'>, '/api/damage-types/*': <class 'dnd5eapy.damagetypes.DamageType'>, '/api/magic-schools': <class 'dnd5eapy.magicschools.MagicSchools'>, '/api/feats/*': <class 'dnd5eapy.feats.Feat'>, '/api/equipment': <class 'dnd5eapy.equipment.Equipment'>}
>>>
```

Note that objects with `url_leaf`'s ending in `"/*"` (such as `'/api/subraces/*'` and `'/api/ability-scores/*'`) are
grandchildren classes of the
base [DnD5eAPIObj](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy/core/__init__.py#L50) class
designed for working with api endpoints that return information on a single item. When calling those class constructors,
you would pass in the corresponding `url_leaf=` argument for the item you want into the constructor's caller. More on
that later.

But before we get to the grandchildren classes, we should look at an example of the direct children classes. Each of
which represents an api node directly after the root node (`"/api"`). All api nodes immediately after the root node
return the same list based response structor. Thus, the children classes are really just copies of the root parent class
with only their default `url_leaf=` argument overriden.

The example child class that we will look at
is [AbilityScores](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy/abilityscores/__init__.py#L39)
which works with data from [ability-scores endpoint](https://www.dnd5eapi.co/api/ability-scores):

```json
{
  "count": 6,
  "results": [
	{
	  "index": "cha",
	  "name": "CHA",
	  "url": "/api/ability-scores/cha"
	},
	{
	  "index": "con",
	  "name": "CON",
	  "url": "/api/ability-scores/con"
	},
	{
	  "index": "dex",
	  "name": "DEX",
	  "url": "/api/ability-scores/dex"
	},
	{
	  "index": "int",
	  "name": "INT",
	  "url": "/api/ability-scores/int"
	},
	{
	  "index": "str",
	  "name": "STR",
	  "url": "/api/ability-scores/str"
	},
	{
	  "index": "wis",
	  "name": "WIS",
	  "url": "/api/ability-scores/wis"
	}
  ]
}
```

You can initiate
an [AbilityScores](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy/abilityscores/__init__.py#L39)
instance directly through its constructor or since we already have
a [DnD5eAPIObj](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy/core/__init__.py#L50) instance
initiate in our example console, we can use the `DnD5eAPIObj.create_instance_from_url` method:

```pycon
>>> ability_scores = dnd.create_instance_from_url(dnd.url_column.at["ability-scores"])
>>> print(ability_scores)
<dnd5eapy.abilityscores.AbilityScores object from https://www.dnd5eapi.co/api/ability-scores at 0x0000021E4DBCD7B8>
>>> print(ability_scores.df)
      name                      url
index                              
cha    CHA  /api/ability-scores/cha
con    CON  /api/ability-scores/con
dex    DEX  /api/ability-scores/dex
int    INT  /api/ability-scores/int
str    STR  /api/ability-scores/str
wis    WIS  /api/ability-scores/wis
>>>
```

All other immediate children classes
of [DnD5eAPIObj](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy/core/__init__.py#L50) will
generate the same two column dataframes indexed by whatever is called out as the `"index"` in the response. Each of
these children have a child class of their own (i.e. the grandchildren classes mentioned earlier) that represent a
single item as opposed to a list of items. Keeping with
our [AbilityScores](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy/abilityscores/__init__.py#L39)
example, we will look at an initiated example of its child
[AbilityScore](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy/abilityscores/__init__.py#L60)
pointed at [ability-scores/dex endpoint](https://www.dnd5eapi.co/api/ability-scores/dex):

```pycon
>>> dex = ability_scores.create_instance_from_url(ability_scores.url_column.at["dex"])
>>> print(dex)
<dnd5eapy.abilityscores.AbilityScore object from https://www.dnd5eapi.co/api/ability-scores/dex at 0x0000021E4CBAA5C0>
>>> print(dex.df)
      name  ...                      url
index       ...                         
dex    DEX  ...  /api/ability-scores/dex
[1 rows x 5 columns]
>>> print(dex.columns)
Index(['name', 'full_name', 'desc', 'skills', 'url'], dtype='object')
>>>
```

All of these grandchildren classes will result in single row dataframes containing a variable number of columns
depending on what the source endpoint is. Since these are single row dataframes, the classes (will*) have unique
properties for getting and setting their values:

**Most of these class properties are still underdevelopment...*

```pycon
>>> print(dex.name)
DEX
>>> print(dex.full_name)
Dexterity
>>> print(dex.desc)
['Dexterity measures agility, reflexes, and balance.'
 'A Dexterity check can model any attempt to move nimbly, quickly, or quietly, or to keep from falling on tricky footing. The Acrobatics, Sleight of Hand, and Stealth skills reflect aptitude in certain kinds of Dexterity checks.']
>>> dex.desc = "\n".join(dex.desc)
>>> print(dex.desc)
Dexterity measures agility, reflexes, and balance.
A Dexterity check can model any attempt to move nimbly, quickly, or quietly, or to keep from falling on tricky footing. The Acrobatics, Sleight of Hand, and Stealth skills reflect aptitude in certain kinds of Dexterity checks.
>>> 
```

Note that since these property getters pull their values from the instance's dataframe, the property setters will
consistently update the corresponding value in the instance's dataframe having downstream effects to all other class
members that also return that property's value.

Some of these grandchildren classes will have columns that contain nested dataframes. That is the case
with [AbilityScore](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy/abilityscores/__init__.py#L60)
objects' skills column:

```pycon
>>> print(dex.skills_column["dex"])
                            name                          url
index                                                        
acrobatics            Acrobatics       /api/skills/acrobatics
sleight-of-hand  Sleight of Hand  /api/skills/sleight-of-hand
stealth                  Stealth          /api/skills/stealth
>>> print(dex.skills_df)
                            name                          url
index                                                        
acrobatics            Acrobatics       /api/skills/acrobatics
sleight-of-hand  Sleight of Hand  /api/skills/sleight-of-hand
stealth                  Stealth          /api/skills/stealth
>>> 
```

Unlike the other properties that do not have dataframes as their raw value, these dataframe properties are named with
a `_df` suffix. That's because invoking the equivalent member name lacking the suffix will return an
appropriate [DnD5eAPIObj](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/dnd5eapy/core/__init__.py#L50)
child object initialized off of that nested dataframe's data:

```pycon
>>> dex_skills = dex.skills
>>> print(dex_skills)
<dnd5eapy.skills.Skills object from https://www.dnd5eapi.co/api/ability-scores/dex at 0x0000021E4DC030B8>
>>> print(dex_skills.df)
                            name                          url
index                                                        
acrobatics            Acrobatics       /api/skills/acrobatics
sleight-of-hand  Sleight of Hand  /api/skills/sleight-of-hand
stealth                  Stealth          /api/skills/stealth
>>> 
```

Most (if not all) of the time , the 'dnd5eapy' object returned by these properties will be a subset of the values that
would be in the object had it been initiated off of the api:

```pycon
>>> skills = dnd5eapy.Skills()
>>> print(skills)
<dnd5eapy.skills.Skills object from https://www.dnd5eapi.co/api/skills at 0x0000021E3C920CC0>
>>> print(skills.df.merge(dex_skills.df, how='left', indicator=True).set_index(skills.index))
                            name                          url     _merge
index                                                                   
acrobatics            Acrobatics       /api/skills/acrobatics       both
animal-handling  Animal Handling  /api/skills/animal-handling  left_only
arcana                    Arcana           /api/skills/arcana  left_only
athletics              Athletics        /api/skills/athletics  left_only
deception              Deception        /api/skills/deception  left_only
history                  History          /api/skills/history  left_only
insight                  Insight          /api/skills/insight  left_only
intimidation        Intimidation     /api/skills/intimidation  left_only
investigation      Investigation    /api/skills/investigation  left_only
medicine                Medicine         /api/skills/medicine  left_only
nature                    Nature           /api/skills/nature  left_only
perception            Perception       /api/skills/perception  left_only
performance          Performance      /api/skills/performance  left_only
persuasion            Persuasion       /api/skills/persuasion  left_only
religion                Religion         /api/skills/religion  left_only
sleight-of-hand  Sleight of Hand  /api/skills/sleight-of-hand       both
stealth                  Stealth          /api/skills/stealth       both
survival                Survival         /api/skills/survival  left_only
>>>
```

Hopefully the intended functionality of these classes is clicking with you by now, and you have a decent idea of what
the library will be capable of once it is complete. I encourage you to clone the repro and play around with the
"Shitty D&D API Browser" app in [main.py](https://github.com/Phillyclause89/DnD5eAPIBrowser/blob/main/main.py):

!["Shitty D&D API Browser"](./demo.gif)


