import tkinter as tk


class LabelTable(tk.Frame):

    def __init__(self, parent, headers):
        # use gray background so it "peeks through" to form grid lines
        tk.Frame.__init__(self, parent, background="gray", padx=1, pady=1)
        self._cells = []
        self._widths = list(headers.values())
        self._headers = list(headers.keys())
        self.insert(self._headers, bg='silver')
        '''for column in range(columns):
            self.grid_columnconfigure(column, weight=1)'''

    def insert(self, row, bg='white'):
        current_row = []
        for ix, col in enumerate(row):
            cell = tk.Label(self,
                            text=col,
                            borderwidth=0,
                            width=self._widths[ix][0],
                            background=bg,
                            anchor=self._widths[ix][1])
            cell.grid(row=len(self._cells), column=ix, padx=1, pady=1)
            current_row.append(cell)
        self._cells.append(current_row)

    def cell_config(self, row, column, values):
        widget = self._cells[row][column]
        widget.configure(values)

