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
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.screenwidth, self.screenheight = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.canvas = tk.Canvas(self.root, scrollregion=f"0 0 {self.screenwidth * 2} {self.screenheight * 20}")
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.orig_x = self.canvas.xview()[0]
        self.orig_y = self.canvas.yview()[0]
        self.butts = self.generate_butts()
        self.back_butt = tk.Button(
            self.canvas,
            text="Back",
            command=self.go_back,
            name="back"
        )

        self.ex_butt = tk.Button(
            self.canvas,
            text="Exit",
            command=self.root.destroy,
            name="exit"
        )
        self.canvas.create_window(0, 0, anchor="nw", window=self.ex_butt)
        self.canvas.create_window(50, 0, anchor="nw", window=self.back_butt)
        self.place_buttons_and_text()
        self.makescroll()
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.bind("<Escape>", self.closer)
        self.root.wm_attributes("-fullscreen", 1)
        self.root.wm_attributes("-top", 1)

    def go_back(self):
        self.dnds.insert(0, self.dnds.pop(-1))
        self.current_dnd = self.dnds[-1]
        [b.destroy() for b in self.butts]
        self.canvas.delete("DeleteMe")
        self.butts = self.generate_butts()
        self.place_buttons_and_text()
        self.canvas.xview_moveto(self.orig_x)
        self.canvas.yview_moveto(self.orig_y)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def place_buttons_and_text(self):
        y = 100
        for butt in self.butts:
            self.canvas.create_window(10, y, anchor="nw", window=butt)
            self.canvas.create_text(
                self.screenwidth // 6, y, anchor="nw",
                text="\n___________________________________\n".join(
                    [
                        f"{'    |   '.join([f'{x}' for x in i]) if isinstance(i, Iterable) else i}    |" for i in
                        self.current_dnd[
                            self.current_dnd.df['url'] == butt._name
                            ].to_dict().items()
                    ]
                ),
                width=2000,
                justify=tk.CENTER,
                tags="DeleteMe",
            )
            y += self.screenheight // 9

    def makescroll(self):
        v = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        v.grid(row=0, column=1, sticky=tk.NS)
        self.canvas.config(yscrollcommand=v.set)
        h = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h.grid(row=1, column=0, sticky=tk.EW)
        self.canvas.config(xscrollcommand=h.set)

    def closer(self, ev):
        self.root.destroy()

    def button_click(self, j):
        const = self.leaf_constructors.get(j, self.leaf_constructors.get("/".join(j.split("/")[:-1]) + "/*"))
        if const not in self.dnds:
            self.dnds.append(const(j))
        else:
            self.dnds.append(self.dnds.pop(self.dnds.index()))
        self.current_dnd = self.dnds[-1]
        [b.destroy() for b in self.butts]
        self.canvas.delete("DeleteMe")
        self.butts = self.generate_butts()
        self.place_buttons_and_text()
        self.canvas.xview_moveto(self.orig_x)
        self.canvas.yview_moveto(self.orig_y)

    def generate_butts(self):
        return [
            tk.Button(
                self.canvas,
                text=f"{i}",
                command=partial(self.button_click, u),
                name=f"{u}",
            ) for i, u in zip(self.current_dnd.df.index, self.current_dnd["url"])
        ]


if __name__ == "__main__":
    Big = BigScreen()
    Big.root.mainloop()
