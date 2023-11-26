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
"""Backgrounds

"""
from dnd5eapy import core


class Backgrounds(core.DnD5eAPIObj):
    """Child class of `DnD5eAPIObj` for handling data out of the backgrounds api.

    Parameters
    ----------
    url_leaf: str, optional
        Overrides the parent's `url_leaf` to target backgrounds api.

    **kwargs: optional
        Keyword arguments to pass to `super().__init__()`


    """
    url_leaf: str = "/api/backgrounds"

    def __init__(self, url_leaf: str = url_leaf, **kwargs) -> None:
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
