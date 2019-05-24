import tkinter as tk


class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.wm_minsize(800, 600)
        headers = {"ORD": (5, "center"),
                   "Nota": (8, "center"),
                   "Nome do(a) aluno(a)": (40, "w"),
                   "Assinatura": (40, "center")}
        t = LabelTable(self, headers)
        t.cell_config(0, 2, {"anchor": "center"})
        t.insert([1, ' ', 'Ana Carolina Kropniczki de Azevedo', ' '])
        t.insert([2, ' ', 'Edson Kropniczki', ' '])
        t.insert([3, '10.0', 'Edson Kropniczki', ' '])
        t.insert([4, '10.0', 'Edson Kropniczki', ' '])
        t.insert([5, '10.0', 'Edson Kropniczki', ' '])


class LabelTable:

    def __init__(self, parent, headers):
        self.wrapF = tk.Frame(parent)
        self.wrapF.grid(row=0, column=0, sticky=tk.NSEW)
        self.wrapF.grid_rowconfigure(0, weight=1)
        self.wrapF.grid_columnconfigure(0, weight=1)

        self.scrollbarF = tk.Frame(self.wrapF)
        self.scrollbarF.grid(row=0, column=1, sticky=tk.NS)
        self.scrollbarF.grid_rowconfigure(0, weight=1)
        self.scrollbar = tk.Scrollbar(self.scrollbarF, orient='vertical')
        self.scrollbar.grid(row=0, column=0, sticky=tk.NS)

        self.canvas = tk.Canvas(self.wrapF, yscrollcommand=self.scrollbar.set)  # do height=100 to try scrolling
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        # use gray background so it "peeks through" to form grid lines
        self.tableF = tk.Frame(self.canvas, background="gray", padx=1, pady=1)
        self.tableF.grid(row=0, column=0, sticky=tk.NSEW)
        self.canvas.create_window((0, 0), window=self.tableF, anchor="nw")      # sehr wichtig!!
        self.scrollbar.config(command=self.canvas.yview)
        self.tableF.bind("<Configure>", self.onFrameConfigure)

        self._cells = []
        self._widths = list(headers.values())
        self._headers = list(headers.keys())
        self.insert(self._headers, bg='silver')
        # set canvas width to table width
        # find out table width by summing widths of each table header cell
        print(2*len(self._cells))
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


if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()


