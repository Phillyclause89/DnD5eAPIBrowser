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

import tkinter as tk
from functools import partial

import DnD5eAPy as DnD


def button_click(j):
    global dnd, butts
    dnd = leaf_constructors[j]()
    [b.destroy() for b in butts]
    butts = generate_butts()
    [b.pack() for b in butts]


def generate_butts():
    global dnd
    return [tk.Button(root, text=f"{i}:{j}", command=partial(button_click, j[0]), name=f"{j}") for i, j in
            zip(dnd.df.index, dnd.df.values)]


if __name__ == "__main__":
    dnd = DnD.DnD5eAPIObj()
    leaf_constructors = DnD.get_leaf_constructor_map()
    root = tk.Tk()
    root.title("DnD5e API Explorer")
    ext_butt = tk.Button(root, text="Exit",
                         command=root.destroy)
    butts = generate_butts()
    [b.pack() for b in butts]
    ext_butt.pack()
    root.mainloop()
