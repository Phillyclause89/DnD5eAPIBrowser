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
    from typing import Any, Dict, Iterable, Iterator, List, Self, Set, Type, Union, Tuple
except ImportError as i_error:
    warn(f"{i_error}", ImportWarning)
    from typing_extensions import Self
    from typing import Any, Dict, Iterator, List, Type, Union, Set, Tuple

import pandas as pd
import requests

DEFAULT_STATUS_CODE_COLUMN_NAME: str = "status_code"
DEFAULT_NAME_COLUMN_NAME: str = "name"
DEFAULT_URL_COLUMN_NAME: str = "url"
DEFAULT_OBJ_COLUMN_NAME: str = "obj"
DEFAULT_INDEX_NAME: str = "index"
DEFAULT_URL_ROOT: str = "https://www.dnd5eapi.co"
DEFAULT_URL_LEAF: str = "/api"
DEFAULT_HEADERS: Dict[str, str] = {'Accept': 'application/json'}


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
    timeout : Union[int, float], optional
        timeout value passed to request.get(timeout)
    data : Any, optional
        Overrides the requests call during object construction and
        populates self with passed in data instead.
    obj_column_name : str, optional
        Declares what the obj column name will be should it be created by DnD5eAPIObj.create_instances_from_urls()
    index_name : str, optional
        Declares what the index name should be per the data in the api.
        Only should be used if working with a custom api server that uses different key names
    name_column_name : str, optional
        Declares what the name column name should be per the data in the api.
        Only should be used if working with a custom api server that uses different key names
    url_column_name : str, optional
        Declares what the url_full column name should be per the data in the api.
        Only should be used if working with a custom api server that uses different key names


    Attributes
    ----------
    df: pandas.DataFrame
        A DataFrame representation of the `json` object returned by `DnD5eAPIObj.__df_from_response__()`.
    leaf_constructors: Dict[str, Type[Self]]
        Dictionary of all dnd5eapy class constructors mapped to their default url_leaf attribute.
    url_root: str
        The api server root of the `url_full`.
    url_leaf: str
        The api function path of the `url_full`.
    requests_args: Dict[str, Union[Dict[str, str], Dict[str, Dict[str, str]]]]
        The keys are 'headers', 'url_full' and 'timeout'
    response: requests.Response
        The `response` object returned by `DnD5eAPIObj.__get_response__()`.

    """
    leaf_constructors: Dict[str, Type[Self]]
    url_root: str = DEFAULT_URL_ROOT
    url_leaf: str = DEFAULT_URL_LEAF
    requests_args: Dict[str, Union[Dict[str, str], Dict[str, Dict[str, str]]]]
    response: requests.Response = requests.Response()
    df: pd.DataFrame = pd.DataFrame(columns=[
        DEFAULT_STATUS_CODE_COLUMN_NAME, DEFAULT_NAME_COLUMN_NAME, DEFAULT_URL_COLUMN_NAME])

    def __init__(self,
                 url_leaf: str = url_leaf,
                 url_root: str = url_root,
                 headers: Dict[str, str] = None,
                 timeout: Union[int, float, None] = None,
                 data: Any = None,
                 name_column_name: str = DEFAULT_NAME_COLUMN_NAME,
                 url_column_name: str = DEFAULT_URL_COLUMN_NAME,
                 obj_column_name: str = DEFAULT_OBJ_COLUMN_NAME,
                 index_name: str = DEFAULT_INDEX_NAME,
                 ) -> None:
        """Constructs the `DnD5eAPIObj` instance
        """
        self.url_leaf = url_leaf
        self.url_root = url_root
        self.requests_args = {
            'headers': DEFAULT_HEADERS if headers is None else headers,
            'url': self.url_full,
            'timeout': timeout
        }
        self.leaf_constructors = get_leaf_constructor_map()
        self._name_column_name = name_column_name
        self._url_column_name = url_column_name
        self._obj_column_name = obj_column_name
        self._index_name = index_name
        if data is not None:
            self.df = pd.DataFrame(data)
        else:
            self.response = self.__get_response__
            self.df = self.dframe

    @property
    def obj_column_name(self) -> str:
        """self._obj_column_name

        Returns
        -------
        str
        """
        return self._obj_column_name

    @obj_column_name.setter
    def obj_column_name(self, name: Union[str, int]):
        if self.obj_column_name in self.columns:
            self.df = self.df.rename(columns={self.obj_column_name: name})
        self._obj_column_name = name

    @property
    def name_column_name(self) -> str:
        """self._name_column_name

        Returns
        -------
        str
        """
        return self._name_column_name

    @name_column_name.setter
    def name_column_name(self, name: Union[str, int]):
        if self.name_column_name in self.columns:
            self.df = self.df.rename(columns={self.name_column_name: name})
        self._name_column_name = name

    @property
    def url_column_name(self) -> str:
        """self._url_column_name

        Returns
        -------
        str
        """
        return self._url_column_name

    @url_column_name.setter
    def url_column_name(self, name: Union[str, int]):
        if self.url_column_name in self.columns:
            self.df = self.df.rename(columns={self.url_column_name: name})
        self._url_column_name = name

    @property
    def obj_column(self) -> pd.Series:
        """self[self.obj_column_name]

        Returns
        -------
        pandas.Series
        """
        try:
            return self[self.obj_column_name]
        except KeyError as kerr:
            raise RuntimeError(f"The `{self.obj_column_name}` column not in self.columns: {self.columns}.\n"
                               "Call create_instances_from_urls to create this column first.") from kerr

    @obj_column.setter
    def obj_column(self, data: pd.Series):
        self[self.obj_column_name] = data
        self.obj_column_name = data.name

    @property
    def name_column(self) -> pd.Series:
        """self[self.name_column_name]

        Returns
        -------
        pandas.Series
        """
        try:
            return self[self.name_column_name]
        except KeyError as kerr:
            raise KeyError(self.name_column_name) from kerr

    @name_column.setter
    def name_column(self, data: pd.Series):
        self[self.name_column_name] = data
        self.name_column_name = data.name

    @property
    def url_column(self) -> pd.Series:
        """self[self.url_column_name]

        Returns
        -------
        pandas.Series
        """
        try:
            return self[self.url_column_name]
        except KeyError as kerr:
            raise KeyError(self.name_column_name) from kerr

    @url_column.setter
    def url_column(self, data: pd.Series):
        self[self.url_column_name] = data
        self.url_column_name = data.name

    @property
    def url_full(self) -> str:
        """f"{self.url_root}{self.url_leaf}"

        Returns
        -------
        str
        """
        return f"{self.url_root}{self.url_leaf}"

    @property
    def empty(self) -> bool:
        """self.df.empty

        Returns
        -------
        bool
        """
        return self.df.empty

    @property
    def shape(self) -> Tuple[int, int]:
        """self.df.shape

        Returns
        -------
        Tuple[int, int]
        """
        return self.df.shape

    @property
    def size(self) -> int:
        """self.df.size

        Returns
        -------
        int
        """
        return self.df.size

    @property
    def ndim(self) -> int:
        """self.df.ndim

        Returns
        -------
        int
        """
        return self.df.ndim

    @property
    def axes(self) -> List:
        """self.df.axes

        Returns
        -------
        List
        """
        return self.df.axes

    @property
    def values(self) -> np.ndarray:
        """self.df.values

        Returns
        -------
        numpy.ndarray
        """
        return self.df.values

    @property
    def dtypes(self) -> pd.Series:
        """self.df.dtypes

        Returns
        -------
        pandas.Series
        """
        return self.df.dtypes

    @property
    def columns(self) -> pd.Index:
        """self.df.columns

        Returns
        -------
        pandas.Index
        """
        return self.df.columns

    @columns.setter
    def columns(self, index: Union[pd.Index, List]):
        org_columns = self.columns
        self.df.columns = index
        props = {getattr(self, p): p for p in dir(self) if p.endswith("_column_name") and not p.startswith("_")}
        for i, name in enumerate(org_columns):
            prop = props.get(name)
            if prop:
                setattr(self, prop, index[i])

    @property
    def index(self) -> pd.Index:
        """self.df.index

        Returns
        -------
        pandas.Index
        """
        return self.df.index

    def refresh(self) -> None:
        """Updates the `DnD5eAPIObj` instance with a new api request.
            The results of the update are dependent on the instance's
            current `url_full` and `header` property values.

        Returns
        -------
        None
        """
        self.response = self.__get_response__
        self.df = self.dframe

    def create_instances_from_nested_urls(self) -> None:
        """TODO: Decide if I want this or not
        Returns
        -------
        None
        """

    def create_instances_from_urls(self) -> None:
        """Attempts to update api urls in the `df` with initialized `DnD5eAPIObj` objects.

        Returns
        -------
        None

        Notes
        -----
        Basically self.df["url"].apply(self.create_instance_from_url)
        """
        if self:
            self[self.obj_column_name] = self[self.url_column_name].apply(self.create_instance_from_url)
            return
        _warn_m: str = f"INVALID RESPONSE STATUS CODE\n'{DEFAULT_STATUS_CODE_COLUMN_NAME}' in columns:\n{self.columns}"
        warn(_warn_m, ResourceWarning, stacklevel=2)

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

    @property
    def __get_response__(self) -> requests.Response:
        """Gets the api request response via `requests`.
            This method is called at initialization
            and when the `refresh` method is called.

            Results of `__get_response__` method calls are dependent
            on the `url_full` and `headers` attributes.

        Returns
        -------
        requests.Response
        """
        return requests.get(**self.requests_args)

    @property
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
        return {DEFAULT_STATUS_CODE_COLUMN_NAME: status_code, self.name_column_name: self.url_leaf,
                self.url_column_name: self.url_leaf}

    @property
    def __df_from_response__(self) -> pd.DataFrame:
        """gets the `df` from `json`.
            If the keys `'count'` and `'results'` are in `json.keys()` then
            the initial DataFrame will be `df = pd.DataFrame(json.get('results'))`,
            otherwise `df = pd.DataFrame([self.json])` will be initialized.

            If the key `'index'` is in `df.columns` then the final DataFrame returned
            will be indexed by that key's value(s) (i.e. `return df.set_index('index')`).

            Results of `__df_from_response__` method calls are dependent on the `json` attribute.

        Returns
        -------
        pandas.DataFrame
            Two-dimensional, size-mutable, potentially heterogeneous tabular data representation
            of the `self.json` object sourced from the API response.
        """
        json: Dict[str, Union[int, Dict[str, Any], List[Any]]] = self.__get_json__
        if json.get('count') and json.get('results'):
            _df: pd.DataFrame = pd.json_normalize(json.get('results'))
            return self.__set_df_index__(_df)
        _df = pd.json_normalize([json])
        if self.response.url == self.requests_args['url'] and self.url_leaf == DEFAULT_URL_LEAF:
            return _df.transpose().rename(columns={0: self.url_column_name}).rename_axis(self._index_name)
        return self.__set_df_index__(_df)

    def __set_df_index__(self, _df: pd.DataFrame) -> pd.DataFrame:
        return _df.set_index(self._index_name) if self._index_name in _df.columns else _df

    def __add_name_column__(self, _df: pd.DataFrame) -> pd.DataFrame:
        if (self.url_column_name in _df.columns) and self.name_column_name not in _df.columns:
            _df[self.name_column_name] = _df[self.url_column_name].str.replace(
                f"{self.url_leaf}/", "").str.replace("-", " ").str.title()
            _df = _df[[self.name_column_name] + [col for col in _df.columns if col != self.name_column_name]]
        return _df

    def __get_sub_dfs__(self, _df: pd.DataFrame) -> pd.DataFrame:
        if _df.shape[0] == 1 and _df.shape[1] > 2:
            for col in (c for c in _df.columns if c not in [self.url_column_name, self.name_column_name]):
                item = _df.at[_df.index[0], col]
                if isinstance(item, list) and len(item) > 0:
                    if isinstance(item[0], Dict):
                        sub_df = pd.json_normalize(item, max_level=5)
                        sub_df = self.__set_df_index__(sub_df)
                        _df.at[_df.index[0], col] = sub_df
                    else:
                        _df.at[_df.index[0], col] = np.array(item)
        return _df

    @property
    def dframe(self) -> pd.DataFrame:
        """returns a new df from the current response json

        Returns
        -------
        DataFrame

        """
        return self.__get_sub_dfs__(self.__add_name_column__(self.__df_from_response__))

    def __getitem__(self, item: Union[str, pd.Series]) -> Union[pd.Series, pd.DataFrame]:
        """Invokes self.df.__getitem__(item)

        Parameters
        ----------
        item : Union[str, pandas.core.series.Series]

        Returns
        -------
        Union[pandas.core.series.Series, pandas.core.frame.DataFrame]
        """
        return self.df.__getitem__(item)

    def __len__(self) -> int:
        """Invokes self.df.__len__()

        Returns
        -------
        int
        """
        return self.df.__len__()

    def __setitem__(self, key: str, value: pd.Series) -> None:
        """Invokes self.df.__setitem__(key, value)

        Parameters
        ----------
        key
        value

        Returns
        -------
        None
        """
        return self.df.__setitem__(key, value)

    def __contains__(self, item: Any) -> bool:
        """self.df.__contains__(item)

        Parameters
        ----------
        item: Any

        Returns
        -------
        bool

        """
        return self.df.__contains__(item)

    def __iter__(self) -> Iterator:
        """self.df.__iter__()

        Returns
        -------
        Any

        """
        return self.df.__iter__()

    def __add__(self, other: Any) -> pd.DataFrame:
        """self.df.__add__(other)

        Parameters
        ----------
        other: Any

        Returns
        -------
        pd.DataFrame

        """
        return self.df.__add__(other)

    def __sub__(self, other: Any) -> pd.DataFrame:
        """self.df.__sub__(other)

        Parameters
        ----------
        other

        Returns
        -------
        pd.DataFrame

        """
        return self.df.__sub__(other)

    def __mul__(self, other: Any) -> pd.DataFrame:
        """self.df.__mul__(other)

        Parameters
        ----------
        other : Any

        Returns
        -------
        pd.DataFrame

        """
        return self.df.__mul__(other)

    def __truediv__(self, other: Any) -> pd.DataFrame:
        """self.df.__truediv__(other)

        Parameters
        ----------
        other

        Returns
        -------
        pd.DataFrame
        """
        return self.df.__truediv__(other)

    def __pow__(self, power: Any, modulo: object = None) -> pd.DataFrame:
        """self.df.__pow__(power, modulo)

        Parameters
        ----------
        power
        modulo

        Returns
        -------
        pd.DataFrame

        """
        return self.df.__pow__(power, modulo)

    def __eq__(self, other: Any) -> pd.DataFrame:
        """self.df.__eq__(other)

        Parameters
        ----------
        other: Any

        Returns
        -------
        DataFrame
        """
        return self.df.__eq__(other)

    def __ne__(self, other: Any) -> pd.DataFrame:
        """self.df.__ne__(other)

        Parameters
        ----------
        other: Any

        Returns
        -------
        DataFrame
        """
        return self.df.__ne__(other)

    def __gt__(self, other: Any) -> pd.DataFrame:
        """self.df.__gt__(other)

        Parameters
        ----------
        other: Any

        Returns
        -------
        DataFrame
        """
        return self.df.__gt__(other)

    def __ge__(self, other: Any) -> pd.DataFrame:
        """self.df.__ge__(other)

        Parameters
        ----------
        other: Any

        Returns
        -------
        DataFrame
        """
        return self.df.__ge__(other)

    def __le__(self, other: Any) -> pd.DataFrame:
        """self.df.__le__(other)

        Parameters
        ----------
        other: Any

        Returns
        -------
        DataFrame
        """
        return self.df.__le__(other)

    def __bool__(self) -> bool:
        """DEFAULT_STATUS_CODE_COLUMN_NAME not in self.columns

        Returns
        -------
        bool
        """
        return DEFAULT_STATUS_CODE_COLUMN_NAME not in self.columns

    def __str__(self) -> str:
        """self.__repr__().replace(" at ", f" from {self.response.url_full} at ")

        Returns
        -------
        str

        """
        return self.__repr__().replace(" at ", f" from {self.url_full} at ")


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
        cls : type

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
