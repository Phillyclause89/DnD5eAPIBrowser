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
#
#  All rights reserved.
#
"""Shitty Browser App

"""
import io
import random
import sys
import tkinter as tk
from collections.abc import Iterable
from functools import partial
from io import BytesIO
from tkinter import Button, Menu, Tk, font
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import pandas as pd
import requests
from PIL import Image, ImageTk, JpegImagePlugin, PngImagePlugin
from pandas import DataFrame, Series
from pandas.core.generic import NDFrame

import dnd5eapy as dnd
from dnd5eapy import DnD5eAPIObj


class BigScreen:
    """Shitty Browser App for figuring out what's in the api.

    """
    title: str
    fullscreen: bool
    butts: Union[List[Button], Any]
    orig_y: float
    orig_x: float
    cascade_label: str
    obj_cascade: Optional[Menu]
    menu_bar: Menu
    font_family: str
    font: Tuple[str, int]
    screenheight: int
    screenwidth: int
    root: Tk
    current_dnd: DnD5eAPIObj
    dnds: List[DnD5eAPIObj]
    leaf_constructors: Dict[str, Any]
    images: Dict[str, Union[Union[DataFrame, Series], Any]]
    current_load_message: str
    loading: bool

    def __init__(self) -> None:
        self.title = "Shitty D&D API Browser"
        self.current_load_message = f"Initializing {self.title}"
        self.obj_cascade = None
        self.root = tk.Tk()
        self.root.config(background='black')
        self.loading = self.loading_update(self.current_load_message)
        random.seed()
        self.images = {}
        self.leaf_constructors = dnd.get_leaf_constructor_map()
        self.dnds = [dnd.DnD5eAPIObj()]
        self.current_dnd = self.dnds[0]
        self.root.title(self.current_load_message)
        self.screenwidth, self.screenheight = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{3 * (self.screenwidth // 5)}x{self.screenheight - 250}")

        self.current_load_message = f"Rolling Initial Font for {self.title}"
        self.loading_update(self.current_load_message)
        self.font, self.font_family = self.roll_new_font()

        self.current_load_message = f"Building Menu Bar for {self.title}"
        self.loading_update(self.current_load_message)
        self.menu_bar = tk.Menu(self.root, font=self.font)
        self.menu_bar.add_command(label="Exit (F5)", font=self.font, command=self.root.destroy)
        self.menu_bar.add_command(label="Toggle Fullscreen (Esc)", font=self.font, command=self.full_screen_toggle)
        self.dnds[-1]["images"] = self.dnds[-1]["url"].apply(self.get_images)
        self.menu_bar.add_command(label="Roll New Font (SHIFT + f)", font=self.font,
                                  command=lambda: self.loading_guard(self.roll_font_click))
        self.menu_bar.add_command(label="Back (BackSpace)", font=self.font,
                                  command=lambda: self.loading_guard(self.go_back))

        self.obj_cascade, self.cascade_label = self.generate_obj_cascade()
        self.menu_bar.add_cascade(
            label=self.cascade_label, menu=self.obj_cascade
        )
        self.root.config(menu=self.menu_bar)

        self.current_load_message = f"Building Canvas for {self.title}"
        self.loading_update(self.current_load_message)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        # noinspection PyTypeChecker,PydanticTypeChecker
        self.canvas = tk.Canvas(
            self.root,
            scrollregion=f"0 0 {self.screenwidth * 2} {self.screenheight * 100}",
            background="#D4F1F4"
        )
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.orig_x = self.canvas.xview()[0]
        self.orig_y = self.canvas.yview()[0]
        self.butts = self.generate_butts()
        self.place_buttons_and_text()
        self.make_scroll()

        self.current_load_message = f"Binding Commands for {self.title}"
        self.loading_update(self.current_load_message)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.bind("<F5>", self.closer)
        self.root.bind("<BackSpace>", lambda e: self.loading_guard(self.go_back, e))
        self.root.bind("<F>", lambda e: self.loading_guard(self.roll_font_click, e))
        self.fullscreen = False
        self.root.wm_attributes("-fullscreen", self.fullscreen)
        self.root.bind("<Escape>", self.full_screen_toggle)
        self.root.wm_attributes("-top", self.fullscreen)

        self.current_load_message = ""
        self.root.title(self.title)
        self.menu_bar.entryconfigure(tk.END, label=self.cascade_label, font=self.font)
        self.loading = False

    def loading_guard(self, func: Callable, *args) -> Any:
        """

        Returns
        -------
        Any
        """
        if not self.loading:
            return func(*args)

    def loading_update(self, f_text: Any) -> bool:
        """
        Parameters
        ----------
        f_text : Any

        Returns
        -------
        bool

        """
        self.loading = True
        self.current_load_message = f"{f_text}"
        if self.obj_cascade:
            self.menu_bar.entryconfigure(tk.END, label=self.current_load_message, font=self.font)
        self.root.title(f"{self.title}: {f_text}")
        self.root.update()
        return self.loading

    def roll_new_font(self) -> Tuple[Tuple[str, int], str]:
        """

        Returns
        -------
        Tuple[Tuple[str, int], str]
        """
        self.font_family = random.choice(list(font.families()))
        self.font = (self.font_family, random.randint(8, 15))
        self.root.option_add("*Font", self.font)
        return self.font, self.font_family

    def roll_font_click(self, _: Any = None) -> None:
        self.clear_page()
        m = "New Font"
        self.loading_update(m)
        self.roll_new_font()
        self.loading_update(f"{m}: {self.font_family}")
        self.update_page()
        self.loading = False

    def full_screen_toggle(self, _=None):
        self.fullscreen = not self.fullscreen
        self.root.wm_attributes("-fullscreen", self.fullscreen)
        self.root.wm_attributes("-top", self.fullscreen)

    def update_page(self) -> None:
        self.current_dnd = self.dnds[-1]
        self.loading_update(f"Fetching images for {self.current_dnd}")
        self.dnds[-1]["images"] = self.dnds[-1]["images"] if "images" in self.dnds[
            -1
        ].dframe.columns else self.dnds[-1]["url"].apply(self.get_images)
        self.loading_update(f"Generating buttons for {self.current_dnd}")
        self.butts = self.generate_butts()
        self.place_buttons_and_text()
        self.loading_update("Updating cascade list")
        self.generate_obj_cascade()
        self.menu_bar.entryconfigure(tk.END, label=self.cascade_label, font=self.font)
        self.root.title(self.title)
        self.current_load_message = ""
        self.root.update()

    def clear_page(self) -> None:
        self.loading_update("Cleaning up current page...")
        self.canvas.xview_moveto(self.orig_x)
        self.canvas.yview_moveto(self.orig_y)
        [b.destroy() for b in self.butts]
        self.canvas.delete("DeleteMe")
        self.obj_cascade.delete(0, "end")
        self.root.update()

    def go_back(self, _: Union[Any, None] = None) -> None:
        self.loading_update(f"Going back to {self.dnds[-2]}")
        self.clear_page()
        self.dnds.insert(0, self.dnds.pop(-1))
        self.update_page()
        self.loading = False

    def _on_mousewheel(self, event: tk.Event) -> None:
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def place_buttons_and_text(self) -> None:
        """place butts

        """
        y: int = self.screenheight // 8
        butt: Union[Button, Any]
        for butt in self.butts:
            self.loading_update(f"Building {butt}")
            butt_row_items: Union[Union[Series, DataFrame, None, NDFrame], Any]
            butt_row_items = self.current_dnd[self.current_dnd['url'] == butt._name]
            self.canvas.create_window(self.screenwidth // 12, y, anchor="n", window=butt)
            self.canvas.create_text(
                self.screenwidth // 3, y,
                anchor="n",
                activefill='#027148',
                font=self.font,
                text=self.generate_text(butt_row_items),
                width=self.screenwidth // 2.75,
                justify=tk.CENTER,
                tags=("DeleteMe", f"{butt._name}"),
            )
            image: str = random.choice(butt_row_items["images"].values[0])
            size: Tuple[int, int] = (int(self.screenwidth // 8), self.screenheight // 5)
            if image not in self.images:
                self.loading_update(f"Building image from {image} for {butt}")
                io_image: BytesIO = io.BytesIO(requests.get(image).content)
                pil_img: Image = Image.open(io_image)
                if pil_img.size[0] > pil_img.size[1]:
                    w_percent: float = (size[0] / float(pil_img.size[0]))
                    h_size: int = int((float(pil_img.size[1]) * float(w_percent)))
                    pil_img = pil_img.resize((size[0], h_size), Image.LANCZOS)
                else:
                    h_percent: float = (size[1] / float(pil_img.size[1]))
                    w_size: int = int((float(pil_img.size[0]) * float(h_percent)))
                    pil_img = pil_img.resize((w_size, size[1]), Image.LANCZOS)
                pil_img.seek(0)
                pil_img.save(io_image, format='PNG')
                pil_img.seek(0)
                tk_image: Image = ImageTk.PhotoImage(pil_img, size=size)
            else:
                tk_image = self.images[image]
            butt.config(image=tk_image, width=size[0] - 10, height=size[1] - 10, background="#0000FF")
            self.images[image] = tk_image
            self.canvas.tag_bind(f"{butt._name}", '<ButtonPress-1>', partial(
                lambda e, j=butt._name: self.loading_guard(self.button_click, j, e)
            ))
            y += self.screenheight // 4
            self.loading_update(f"Finished {butt}")
            self.root.update()

    def make_scroll(self) -> None:
        v = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        v.grid(row=0, column=1, sticky=tk.NS)
        self.canvas.config(yscrollcommand=v.set)
        h = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h.grid(row=1, column=0, sticky=tk.EW)
        self.canvas.config(xscrollcommand=h.set)

    def closer(self, _: Any) -> None:
        self.root.destroy()

    def button_click(self, url: str, _=None) -> None:
        """

        Parameters
        ----------        
        url : str
        _ : Any
        
        """
        self.loading_update(f"Loading {url}")
        self.clear_page()
        url_lst: List[str] = url.split("/")
        backup_j: str = "/".join(url_lst[:-1]) + "/*"
        const: Type[DnD5eAPIObj] = self.leaf_constructors.get(url, self.leaf_constructors.get(backup_j))
        search: str = const.url_leaf.replace("/*", f"/{url_lst[-1]}")
        search_result = [i for i, dnd_obj in enumerate(self.dnds) if dnd_obj.url_leaf == search]
        if not search_result:
            self.loading_update(f"Initializing new {const} for {url}")
            dnd_obj = const(url)
            self.dnds.append(dnd_obj)
        else:
            self.dnds.append(self.dnds.pop(search_result[0]))
        self.update_page()
        self.loading = False

    @staticmethod
    def generate_text(butt_row_items: pd.DataFrame) -> str:
        """Generates a text representation of the `butt_row_items` DataFrame.

        Parameters
        ----------
        butt_row_items : pd.DataFrame
            The DataFrame to generate the text representation for.

        Returns
        -------
        str
            The text representation of the `butt_row_items` DataFrame.

        Notes
        -----
        The text representation includes the column names and values for all columns except the `"images"` column.
        """

        def get_sub_sub_value(_value: Union[Iterable, List, Dict], _sub_value: Union[str, int], _i: int):
            """

            Parameters
            ----------
            _value
            _sub_value
            _i

            Returns
            -------

            """
            return f"{_sub_value}: {_value[_sub_value]}\n" if isinstance(_value, dict) else f"{_value[_i]}\n"

        s = ""
        columns_to_include = [c for c in butt_row_items.columns if c != "images"]
        for column in columns_to_include:
            s += f"Column: {column}\n"
            for index, value in butt_row_items[column].items():
                if isinstance(value, Iterable) and not isinstance(value, str):
                    for i, sub_value in enumerate(value):
                        s += get_sub_sub_value(value, sub_value, i)
                else:
                    s += f"Value: {value}\n"
                s += f"Index: {index}\n"
            s += "\n"
        return s

    def generate_butts(self) -> List[tk.Button]:
        butts = []
        for i, u in zip(self.current_dnd.dframe.index, self.current_dnd["url"]):
            self.root.update()
            butts.append(tk.Button(
                self.canvas,
                text=f"{i}",
                command=partial(lambda url=u: self.loading_guard(self.button_click, url)),
                name=f"{u}",
                activebackground='#027148',
                background="#0000FF"
            ))
        return butts

    def generate_obj_cascade(self) -> Union[Menu, Tuple[Menu, str]]:
        """

        Returns
        -------
        Union[tkinter.Menu, Tuple[tkinter.Menu, str]]
        """
        if not self.obj_cascade:
            self.obj_cascade = tk.Menu(self.menu_bar, tearoff=0)
        size_total = 0
        for i, dnd_obj in list(enumerate(self.dnds))[::-1]:
            self.root.update()
            size = ((sys.getsizeof(dnd_obj) + sys.getsizeof(
                dnd_obj.dframe) + sys.getsizeof(
                dnd_obj.response)) / 1024)
            size_total += size
            self.obj_cascade.add_command(
                label=f"{dnd_obj} | Size: {size} (kB)",
                command=lambda ii=i: self.select_loaded(ii),
                font=self.font
            )
        self.cascade_label = f"DnDObjs Loaded: {len(self.dnds)} Size: {size_total} (kB)"
        return self.obj_cascade, self.cascade_label

    def select_loaded(self, i):
        self.loading_update(f"Loading {self.dnds[i]}")
        self.clear_page()
        self.dnds.append(self.dnds.pop(i))
        self.update_page()
        self.loading = False

    def get_images(
            self,
            url_leaf: str = None
    ) -> Union[None, List[JpegImagePlugin.JpegImageFile], List[PngImagePlugin.PngImageFile], List[str], List]:
        if url_leaf is None:
            url_leaf = self.current_dnd.url_leaf
        term = "+".join(url_leaf.split("/")[2:]).replace("-", "+")
        self.loading_update(f"Searching google images for Dungeons+and+Dragons+{term}")
        google_url = f"https://www.google.co.in/search?site=imghp&q=Dungeons+and+Dragons+{term}&tbs=il:cl&tbm=isch"
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/43.0.2357.134 Safari/537.36 "
        }
        response = requests.get(google_url, headers)
        io_images = [x.split('"')[-1] for x in response.text.split(";") if
                     "https://encrypted-tbn0.gstatic.com/images?q=" in x]
        self.loading_update(f"Found {len(io_images)} images!")
        self.root.update()
        return io_images


if __name__ == "__main__":
    Big = BigScreen()
    Big.root.mainloop()
