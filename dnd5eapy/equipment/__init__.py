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
"""Equipment

"""
from dnd5eapy import core


class Equipment(core.DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the equipment api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target equipment api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/equipment"

    def __init__(self, url_leaf: str = url_leaf, **kwargs: object) -> None:
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
