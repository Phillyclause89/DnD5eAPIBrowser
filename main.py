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
#  MIT License
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#
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
#
import sys
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
#
import tkinter as tk
from collections.abc import Iterable
from functools import partial

import DnD5eAPy as DnD


class BigScreen:
    def __init__(self):
        self.leaf_constructors = DnD.get_leaf_constructor_map()
        self.dnds = [DnD.DnD5eAPIObj()]
        self.current_dnd = self.dnds[0]

        self.root = tk.Tk()
        self.menu_bar = tk.Menu(self.root)
        self.menu_bar.add_command(label="Exit (F5)", command=self.root.destroy)
        self.menu_bar.add_command(label="Toggle Fullscreen (Esc)", command=self.full_screen_toggle)
        self.menu_bar.add_command(label="Back", command=self.go_back)
        self.obj_cascade = self.generate_obj_cascade()
        self.root.config(menu=self.menu_bar)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.screenwidth, self.screenheight = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.canvas = tk.Canvas(self.root, scrollregion=f"0 0 {self.screenwidth * 2} {self.screenheight * 20}")
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.orig_x = self.canvas.xview()[0]
        self.orig_y = self.canvas.yview()[0]
        self.butts = self.generate_butts()
        self.place_buttons_and_text()
        self.make_scroll()
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.bind("<F5>", self.closer)
        self.root.bind("<BackSpace>", self.go_back)
        self.fullscreen = True
        self.root.wm_attributes("-fullscreen", self.fullscreen)
        self.root.bind("<Escape>", self.full_screen_toggle)
        self.root.wm_attributes("-top", self.fullscreen)

    def full_screen_toggle(self, _=None):
        self.fullscreen = not self.fullscreen
        self.root.wm_attributes("-fullscreen", self.fullscreen)
        self.root.wm_attributes("-top", self.fullscreen)

    def clean_up(self):
        self.current_dnd = self.dnds[-1]
        [b.destroy() for b in self.butts]
        self.canvas.delete("DeleteMe")
        self.butts = self.generate_butts()
        self.place_buttons_and_text()
        self.canvas.xview_moveto(self.orig_x)
        self.canvas.yview_moveto(self.orig_y)

    def go_back(self, _=None):
        self.dnds.insert(0, self.dnds.pop(-1))
        self.clean_up()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def place_buttons_and_text(self):
        y = 100
        for butt in self.butts:
            self.canvas.create_window(10, y, anchor="nw", window=butt)
            self.canvas.create_text(
                self.screenwidth // 6, y, anchor="nw",
                text="\n__\n".join(
                    [
                        '\n____\n'.join(
                            [
                                '\n______\n'.join(
                                    [
                                        y for y in x
                                    ]
                                ) if isinstance(x, Iterable) and not isinstance(x, str) else x for x in i
                            ]
                        ) if isinstance(i, Iterable) else i for i in self.current_dnd[
                        self.current_dnd.df['url'] == butt._name
                        ].to_dict().items()
                    ]
                ),
                width=self.screenwidth // 2,
                justify=tk.CENTER,
                tags="DeleteMe",
            )
            y += self.screenheight // 9

    def make_scroll(self):
        v = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        v.grid(row=0, column=1, sticky=tk.NS)
        self.canvas.config(yscrollcommand=v.set)
        h = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h.grid(row=1, column=0, sticky=tk.EW)
        self.canvas.config(xscrollcommand=h.set)

    def closer(self, _):
        self.root.destroy()

    def button_click(self, j):
        j_lst = j.split("/")
        backup_j = "/".join(j_lst[:-1]) + "/*"
        const = self.leaf_constructors.get(j, self.leaf_constructors.get(backup_j))
        search = const.url_leaf.replace("/*", f"/{j_lst[-1]}")
        search_result = [i for i, dnd in enumerate(self.dnds) if dnd.url_leaf == search]
        if not search_result:
            dnd = const(j)
            self.dnds.append(dnd)
            self.obj_cascade.destroy()
            self.menu_bar.delete(tk.END)
            self.generate_obj_cascade()
        else:
            self.dnds.append(self.dnds.pop(search_result[0]))
        self.clean_up()

    def generate_butts(self):
        return [
            tk.Button(
                self.canvas,
                text=f"{i}",
                command=partial(self.button_click, u),
                name=f"{u}",
            ) for i, u in zip(self.current_dnd.df.index, self.current_dnd["url"])
        ]

    def generate_obj_cascade(self):
        self.obj_cascade = tk.Menu(self.menu_bar, tearoff=0)
        [self.obj_cascade.add_command(
            label=f"{dnd} | Size kB: {(sys.getsizeof(dnd) + sys.getsizeof(dnd.df) + sys.getsizeof(dnd.json) + sys.getsizeof(dnd.response)) / 1024}"
        ) for dnd in self.dnds[::-1]]
        self.menu_bar.add_cascade(label=f"DnD Objects Loaded: {len(self.dnds)}", menu=self.obj_cascade)
        return self.obj_cascade


if __name__ == "__main__":
    Big = BigScreen()
    Big.root.mainloop()
