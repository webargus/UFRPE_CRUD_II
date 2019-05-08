
from tkinter import *
import tkinter.ttk as ttk


class TreeViewTable:

    def __init__(self, frame, headers):
        colnames = list(headers.keys())
        colwidths = list(headers.values())
        self.tree = ttk.Treeview(frame, columns=colnames[1:], selectmode='extended')
        self.tree.grid({"row": 0, "column": 0, "sticky": NSEW})
        #   acrescenta barras de rolagem
        tree_scroll = ttk.Scrollbar(frame, orient=HORIZONTAL, command=self.tree.xview)
        tree_scroll.grid({"row": 1, "column": 0, "sticky": (W, E)})
        self.tree.configure(xscrollcommand=tree_scroll.set)
        # insere cabeçalhos e define suas larguras
        for ix, header in enumerate(colnames):
            self.tree.heading("#{}".format(ix), text=header)
            self.tree.column("#{}".format(ix), minwidth=colwidths[ix], width=colwidths[ix], stretch=NO)

    def appendItem(self, data, pos=''):
        self.tree.insert(pos, 'end', text=data[0], values=data[1:])





