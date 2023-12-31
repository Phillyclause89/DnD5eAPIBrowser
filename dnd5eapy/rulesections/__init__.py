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
"""RuleSections

"""
from dnd5eapy import core


class RuleSections(core.DnD5eAPIObj):
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
