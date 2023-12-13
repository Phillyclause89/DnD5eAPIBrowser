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
"""Base parent class for most dnd5eapy classes
"""

from _warnings import warn

import numpy as np

try:
    from typing import Any, Dict, Iterable, Iterator, List, Self, Set, Type, Union
except ImportError as i_error:
    warn(f"{i_error}", ImportWarning)
    from typing_extensions import Self
    from typing import Any, Dict, Iterator, List, Type, Union, Set

import pandas as pd
import requests


class DnD5eAPIObj:
    """Base parent class for most dnd5eapy classes.

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
    dframe: pandas.DataFrame
        DataFrame representation of the `json` object returned by `DnD5eAPIObj.__get_df__()`.
    response: requests.Response
        The `response` object returned by `DnD5eAPIObj.__get_response__()`.
    url_root: str
        The api server root of the `url`.
    url_leaf: str
        The api function path of the `url`.
    headers: Dict[str, str]
        The headers used in the api request.
    """
    leaf_constructors: Dict[str, Type[Self]]
    url_root: str = "https://www.dnd5eapi.co"
    url_leaf: str = "/api"
    requests_args: Dict[str, Union[Dict[str, str], Dict[str, Dict[str, str]]]]
    dframe: pd.DataFrame = pd.DataFrame(columns=["name", "url"])
    columns: pd.Index = dframe.columns
    response: requests.Response = requests.Response()

    def __init__(self, url_leaf: str = url_leaf, url_root: str = url_root,
                 headers: Dict[str, str] = None, timeout=None) -> None:
        """Constructs the `DnD5eAPIObj` instance
        """
        self.url_leaf = url_leaf
        self.url_root = url_root
        self.requests_args = {
            'headers': {'Accept': 'application/json'} if headers is None else headers,
            'url': f"{self.url_root}{self.url_leaf}",
            "timeout": timeout
        }
        self.timeout = timeout
        self.leaf_constructors = get_leaf_constructor_map()
        self.response = self.__get_response__()
        self.dframe = self.get_df_from_json()
        self.columns = self.dframe.columns

    def refresh(self) -> None:
        """Updates the `DnD5eAPIObj` instance with a new api request.
            The results of the update are dependent on the instance's
            current `url` and `header` property values.

        Returns
        -------
        None
        """
        self.response = self.__get_response__()
        self.dframe = self.get_df_from_json()
        self.columns = self.dframe.columns

    def create_instances_from_nested_urls(self) -> None:
        """
        Returns
        -------
        None
        """

    def create_instances_from_urls(self) -> None:
        """Attempts to update api urls in the `dframe` with initialized `DnD5eAPIObj` objects.

        Returns
        -------
        None

        Notes
        -----
        Basically self.dframe["url"].apply(self.create_instance_from_url)
        """
        _error: KeyError
        _warn_m: str
        try:
            self.dframe["obj"] = self.dframe["url"].apply(self.create_instance_from_url)
        except KeyError as _error:
            if _error.args[0] == "url":
                _warn_m = (f"INVALID RESPONSE STATUS CODE\nThe "
                           f"DataFrame does not contain a 'url' column:\n{self.dframe.columns}")
                warn(_warn_m, ResourceWarning, stacklevel=2)
                return
            raise _error

    def create_instance_from_url(self, url_leaf: str = url_leaf, **kwargs) -> Self:
        """Searches `DnD5eAPIObj` children to init new instance matching url_leaf pattern

        Parameters
        ----------
        url_leaf : str
            url_leaf used to identify the best `DnD5eAPIObj` class type to create new instance from.
        kwargs

        Returns
        -------
        object

        Notes
        -----
        I know I could probably do this better with regex, but I hate regex.
        """
        split_leaf: List[str] = url_leaf.split("/")
        return self.leaf_constructors.get(
            url_leaf, self.leaf_constructors.get(
                "/".join(split_leaf[:-1]) + "/*", self.leaf_constructors.get(
                    "/".join(split_leaf[:-2]) + "/*", self.__new__
                )
            )
        )(url_leaf, **kwargs)

    def __get_response__(self) -> requests.Response:
        """Gets the api request response via `requests`.
            This method is called at initialization
            and when the `refresh` method is called.

            Results of `__get_response__` method calls are dependent
            on the `url` and `headers` attributes.

        Returns
        -------
        requests.Response
        """
        return requests.get(**self.requests_args)

    def __get_json__(self) -> Dict[str, Union[int, Dict[str, Any], List[Any]]]:
        """Gets the json decoded content of `response`.
            This method is called at initialization and when the `refresh` method is called.

            If `response.status_code` does not equal `200`
            then `{"status_code": response.status_code}` is returned.

            Results of `__get_json__` method calls are dependent on the `response` attribute.

        Returns
        -------
        Dict[str, Union[int, Dict[str, Any], List[Any]]]
            json decoded content of `response.json()` or `{"status_code": response.status_code}`.
        """
        status_code: int = self.response.status_code
        if status_code == 200:
            return self.response.json()
        return {"status_code": status_code}

    def __eq__(self, other: Any) -> pd.DataFrame:
        """

        Parameters
        ----------
        other: Any

        Returns
        -------
        DataFrame
        """
        return self.dframe.__eq__(other)

    def __bool__(self) -> Union[bool, ValueError]:
        """

        Returns
        -------
        Union[bool, ValueError]
        """
        if self.dframe.columns[0] == "status_code":
            return False
        return self.dframe.__bool__()

    def __str__(self) -> str:
        """Returns self.__repr__().replace(" at ", f" from {self.response.url} at ")

        Returns
        -------
        str

        """
        return self.__repr__().replace(" at ", f" from {self.response.url} at ")

    def __get_df__(self) -> pd.DataFrame:
        """gets the `dframe` from `json`.
            If the keys `'count'` and `'results'` are in `json.keys()` then
            the initial DataFrame will be `dframe = pd.DataFrame(json.get('results'))`,
            otherwise `dframe = pd.DataFrame([self.json])` will be initialized.

            If the key `'index'` is in `dframe.columns` then the final DataFrame returned
            will be indexed by that key's value(s) (i.e. `return dframe.set_index('index')`).

            Results of `__get_df__` method calls are dependent on the `json` attribute.

        Returns
        -------
        pandas.DataFrame
            Two-dimensional, size-mutable, potentially heterogeneous tabular data representation
            of the `self.json` object sourced from the API response.
        """
        json: Dict[str, Union[int, Dict[str, Any], List[Any]]] = self.__get_json__()
        if json.get('count') and json.get('results'):
            _df: pd.DataFrame = pd.json_normalize(json.get('results'))
            return self.__set_df_index__(_df)
        _df = pd.json_normalize([json])
        if self.response.url == self.requests_args['url'] and self.url_leaf == "/api":
            return _df.transpose().rename(columns={0: "url"}).rename_axis("index")
        return self.__set_df_index__(_df)

    @staticmethod
    def __set_df_index__(_df):
        return _df.set_index("index") if 'index' in _df.columns else _df

    @staticmethod
    def __add_name_column__(_df):
        if ("url" in _df.columns) and "name" not in _df.columns:
            _df["name"] = _df["url"].str.replace("/api/", "").str.replace("-", " ").str.title()
            _df = _df[['name'] + [col for col in _df.columns if col != 'name']]
        return _df

    def __get_sub_dfs__(self, _df):
        if _df.shape[0] == 1 and _df.shape[1] > 2:
            for col in (c for c in _df.columns if c not in ['url', 'name']):
                item = _df.at[_df.index[0], col]
                if isinstance(item, list) and len(item) > 0:
                    if isinstance(item[0], Dict):
                        sub_df = pd.json_normalize(item, max_level=5)
                        sub_df = self.__set_df_index__(sub_df)
                        _df.at[_df.index[0], col] = sub_df
                    else:
                        _df.at[_df.index[0], col] = np.array(item)
        return _df

    def get_df_from_json(self) -> pd.DataFrame:
        """Invokes `__get_df__`

        Returns
        -------
        DataFrame

        """
        _df: pd.DataFrame = self.__get_sub_dfs__(
            self.__add_name_column__(
                self.__get_df__()
            )
        )
        return _df

    def __getitem__(self, item: Union[str, pd.Series]) -> Union[pd.Series, pd.DataFrame]:
        """Invokes self.dframe.__getitem__(item)

        Parameters
        ----------
        item : Union[str, pandas.core.series.Series]

        Returns
        -------
        Union[pandas.core.series.Series, pandas.core.frame.DataFrame]
        """
        return self.dframe.__getitem__(item)

    def __len__(self) -> int:
        """Invokes self.dframe.__len__()

        Returns
        -------
        int
        """
        return self.dframe.__len__()

    def __setitem__(self, key: str, value: pd.Series) -> None:
        """Invokes self.dframe.__setitem__(key, value)

        Parameters
        ----------
        key
        value

        Returns
        -------
        None
        """
        return self.dframe.__setitem__(key, value)

    def __contains__(self, item: Any) -> bool:
        """self.dframe.__contains__(item)

        Parameters
        ----------
        item: Any

        Returns
        -------
        bool

        """
        return self.dframe.__contains__(item)

    def __iter__(self) -> Iterator:
        """self.dframe.__iter__()

        Returns
        -------
        Any

        """
        return self.dframe.__iter__()

    def __add__(self, other: Any) -> pd.DataFrame:
        """

        Parameters
        ----------
        other: Any

        Returns
        -------
        pd.DataFrame

        """
        return self.dframe.__add__(other)

    def __sub__(self, other: Any) -> pd.DataFrame:
        """

        Parameters
        ----------
        other

        Returns
        -------
        pd.DataFrame

        """
        return self.dframe.__sub__(other)

    def __mul__(self, other: Any) -> pd.DataFrame:
        """

        Parameters
        ----------
        other : Any

        Returns
        -------
        pd.DataFrame

        """
        return self.dframe.__mul__(other)

    def __truediv__(self, other: Any) -> pd.DataFrame:
        """

        Parameters
        ----------
        other

        Returns
        -------
        pd.DataFrame
        """
        return self.dframe.__truediv__(other)

    def __pow__(self, power: Any, modulo: object = None) -> pd.DataFrame:
        """

        Parameters
        ----------
        power
        modulo

        Returns
        -------
        pd.DataFrame

        """
        return self.dframe.__pow__(power, modulo)


def get_leaf_constructor_map(root_class: Type[DnD5eAPIObj] = DnD5eAPIObj) -> Dict[str, Type[Union[DnD5eAPIObj, Any]]]:
    """Gets a dictionary of all dnd5eapy class constructors
    mapped to their default url_leaf attribute.

    Returns
    -------
    Dict[str, Type[DnD5eAPIObj]]
    """

    def all_subclasses(cls: Type[DnD5eAPIObj]) -> Set[Union[Type[DnD5eAPIObj], Any]]:
        """Recursively search for all subclasses

        Parameters
        ----------
        cls : Type[DnD5eAPIObj]

        Returns
        -------
        Set[Type[DnD5eAPIObj]]
        """
        subclass: Type[DnD5eAPIObj]
        subclasses: Set[Type[Union[DnD5eAPIObj, Any]]] = set(cls.__subclasses__())
        for subclass in subclasses.copy():
            subclasses = subclasses.union(all_subclasses(subclass))
        return subclasses

    return {
        **{DnD5eAPIObj.url_leaf: DnD5eAPIObj},
        **{cls.url_leaf: cls for cls in all_subclasses(root_class)}
    }
