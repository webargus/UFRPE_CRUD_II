
from tkinter import *
import tkinter.ttk as ttk


class TreeViewTable:

    def __init__(self, frame, headers):
        print("headers=", headers[1:])
        self.tree = ttk.Treeview(frame, columns=headers[1:], selectmode='extended')
        self.tree.grid({"row": 0, "column": 0})
        tree_scroll = ttk.Scrollbar(frame, orient=HORIZONTAL, command=self.tree.xview)
        tree_scroll.grid({"row": 1, "column": 0, "sticky": (W, E)})
        self.tree.configure(xscrollcommand=tree_scroll.set)
        for ix, header in enumerate(headers):
            self.tree.heading("#{}".format(ix), text=header)

    def appendItem(self, data, pos=''):
        self.tree.insert(pos, 'end', text=data[0], values=data[1:])





