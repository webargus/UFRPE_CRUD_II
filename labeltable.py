"""
    *************************************************************************
    *                                                                       *
    *   Project CRUD II / Sistema de Controle Acadêmico Simplificado        *
    *                                                                       *
    *   Developer: Edson Kropniczki - BSI - 2019.1  - (c)2019               *
    *                                                                       *
    *   class LabelTable                                                    *
    *   Purpose: create table-like GUI to output 'ata' student data;        *
    *   What it does: stacks up tkinter Labels into rows and columns;       *
    *                 shows tabled data as Label texts;                     *
    *                 Labels piled up in a Canvas obj fitted with           *
    *                 a vertical Scrollbar                                  *
    *                                                                       *
    *   Usage: table = LabelTable(parent, headers)                          *
    *   @params:                                                            *
    *   parent = owner of widget                                            *
    *   headers = {"header caption 1": (width, anchor), ... } , where       *
    *             width = header column width,                              *
    *             anchor = text anchorage in table cell (Label); values are *
    *                      standard tkinter W, E or CENTER                  *
    *                                                                       *
    *   DISCLAIMER: Use it on your own risk!                                *
    *                                                                       *
    *************************************************************************
"""

import tkinter as tk


class LabelTable:

    def __init__(self, parent, headers):
        # create frame to wrap both, Canvas and Scrollbar
        self.wrapF = tk.Frame(parent)
        # make frame spread to take up all available space in parent
        self.wrapF.grid(row=0, column=0, sticky=tk.NSEW)
        self.wrapF.grid_rowconfigure(0, weight=1)

        # create frame to hold Scrollbar
        self.scrollbarF = tk.Frame(self.wrapF)
        # assign right column of wrapping frame to Scrollbar frame
        # and stretch it North-South
        self.scrollbarF.grid(row=0, column=1, sticky=tk.NS)
        self.scrollbarF.grid_rowconfigure(0, weight=1)
        self.scrollbarF.grid_columnconfigure(0, weight=0)
        # add vertical Scrollbar to its frame
        self.scrollbar = tk.Scrollbar(self.scrollbarF, orient='vertical')
        self.scrollbar.grid(row=0, column=0, sticky=tk.NS)
        self.scrollbar.grid_columnconfigure(0, weight=0)

        # create Canvas, where we'll pile our table rows and columns,
        # and configure Scrollbar to work with it
        self.canvas = tk.Canvas(self.wrapF, yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        # use gray background so it "peeks through" to form grid lines
        self.tableF = tk.Frame(self.canvas, background="gray", padx=1, pady=1)
        self.tableF.grid(row=0, column=0)
        self.canvas.create_window((0, 0), window=self.tableF, anchor="nw")      # sehr wichtig!!
        self.scrollbar.config(command=self.canvas.yview)
        self.tableF.bind("<Configure>", self.onFrameConfigure)

        # create 'private' member to hold table cells (Labels)
        self._cells = []
        # get widths of columns
        self._widths = list(headers.values())
        # get header captions
        self._headers = list(headers.keys())
        # insert header
        self.insert(self._headers, bg='silver')
        # set canvas width to table width
        # find out table width by summing widths of each table header cell
        table_width = sum([x.winfo_width() for x in self._cells[0]]) + 2*len(self._cells[0]) - 2
        self.canvas.config(width=table_width)

    def onFrameConfigure(self, event):
        # Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def insert(self, row, bg='white'):
        current_row = []
        for ix, col in enumerate(row):
            cell = tk.Label(self.tableF,
                            text=col,
                            borderwidth=0,
                            width=self._widths[ix][0],
                            background=bg,
                            anchor=self._widths[ix][1])
            cell.grid(row=len(self._cells), column=ix, padx=1, pady=1)
            cell.grid_columnconfigure(0, weight=1)
            current_row.append(cell)
        self._cells.append(current_row)
        self.tableF.update_idletasks()

    def cell_config(self, row, column, values):
        widget = self._cells[row][column]
        widget.configure(values)







