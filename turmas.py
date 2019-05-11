from tkinter import *
import treeviewtable as tv
import tools


class Turmas:

    def __init__(self, parent):

        frame = Frame(parent)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=0)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid({"row": 0, "column": 1, "sticky": NSEW, "padx": 4, "pady": 4})

        # top class registry form
        ftop = LabelFrame(frame, {"pady": 8, "padx": 8, "text": " Cadastro de Turma "})
        ftop.grid({"row": 0, "column": 0, "sticky": NSEW})
        Label(ftop, {"text": "Código:"}).grid({"row": 0, "column": 0})
        Entry(ftop, {"width": 4}).grid({"row": 0, "column": 1})
        Label(ftop, {"text": "Período:"}).grid({"row": 0, "column": 2})
        Entry(ftop, {"width": 5}).grid({"row": 0, "column": 3})
        Label(ftop, {"text": "Disciplina:"}).grid({"row": 0, "column": 4})
        ftop.grid_columnconfigure(5, weight=1)
        Label(ftop, {"relief": SUNKEN}).grid({"row": 0, "column": 5, "columnspan": 4, "sticky": EW})

        # professors' frame
        fprofs = LabelFrame(ftop, {"pady": 4, "padx": 4, "text": " Professor(es) "})
        fprofs.grid({"row": 1, "column": 0, "columnspan": 6, "sticky": EW})
        fprofs.grid_columnconfigure(0, weight=1)
        Listbox(fprofs, {"height": 3}).grid({"row": 0, "column": 0, "sticky": EW})
        Button(fprofs, {"text": "X", "padx": 4}).grid({"row": 0, "column": 1, "padx": 4})

        # form ok/delete buttons
        Button(ftop, {"text": "Ok", "width": 10}).grid({"row": 1, "column": 7, "padx": 4})
        Button(ftop, {"text": "Excluir", "width": 10}).grid({"row": 1, "column": 8})

        fbottom = Frame(frame)
        # make row 0 of fbottom extend vertically to take up the whole vertical space available
        # in parent Frame row (row 1 of frame obj)
        fbottom.grid_rowconfigure(0, weight=1)
        # tells parent Frame obj (== frame) that fbottom goes inside cell (row=1, col=0) of frame obj
        fbottom.grid({"row": 1, "column": 0, "sticky": NSEW})

        self.tree = tv.TreeViewTable(fbottom, {"Código": 50, "Período": 100, "Código Disciplina": 70, "Disciplina": 300})










