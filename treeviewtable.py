
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
        self.callback = None
        self.tree.bind('<<TreeviewSelect>>', self._handle_select)

    def appendItem(self, data, pos='', iid=None):
        self.tree.insert(pos, 'end', iid, text=data[0], values=data[1:])

    def clear(self):
        self.tree.delete(*self.tree.get_children())

    def on_select(self, callback):
        self.callback = callback

    def _handle_select(self, event):
        if self.callback is None:
            return
        self.callback(self.get_selection())

    def get_selection(self):
        selection = self.tree.selection()
        ret = []
        for iid in selection:
            dict = self.tree.item(iid)      # lê dados da seleção em dicionário
            dict.update({'iid': iid})       # acrescenta id (chave primária) da seleção
            ret.append(dict)
        return ret


