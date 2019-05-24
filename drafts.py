import tkinter as tk


class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        headers = {"ORD": (5, "center"),
                   "Nota": (8, "center"),
                   "Nome do(a) aluno(a)": (40, "w"),
                   "Assinatura": (40, "center")}
        t = LabelTable(self, headers)
        t.grid(row=0, column=0)
        t.cell_config(0, 2, {"anchor": "center"})
        t.insert([1, ' ', 'Ana Carolina Kropniczki de Azevedo', ' '])
        t.insert([2, ' ', 'Edson Kropniczki', ' '])


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


if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()


