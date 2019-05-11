

from tkinter import *
import treeviewtable as tv


class PainelProfessores:

    def __init__(self, frame):

        frame.grid_rowconfigure(0, weight=0)    # 0 => row won't expand vertically if there's space for that
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # cria frame p/ formulário de cadastro de professor
        fProf = LabelFrame(frame, {"pady": 8, "padx": 8, "text": " Cadastro "})
        fProf.grid({"row": 0, "column": 0, "sticky": NSEW, "pady": 8, "padx": 8})
        fProf.grid_columnconfigure(4, weight=1)    # expande formulário na horizontal até bordas da janela
        Label(fProf, {"text": "Nome:"}).grid({"row": 0, "column": 0})
        self.nomeEdit = Entry(fProf).grid({"row": 0, "column": 1, "columnspan": 5, "sticky": (W, E)})
        Label(fProf, {"text": "CPF:"}).grid({"row": 1, "column": 0, "sticky": W})
        self.cpfEdit = Entry(fProf).grid({"row": 1, "column": 1, "sticky": W})
        Label(fProf, {"text": "Departamento:"}).grid({"row": 1, "column": 2, "sticky": W, "padx": 8})
        self.depEdit = Entry(fProf, {"width": 30}).grid({"row": 1, "column": 3, "sticky": W})
        self.submitBtn = Button(fProf, {"text": "Ok", "width": 10}).grid({"row": 1, "column": 4, "pady": 8, "sticky": E})
        self.delBtn = Button(fProf, {"text": "Excluir", "width": 10}).grid({"row": 1, "column": 5, "pady": 8, "padx": 8, "sticky": E})

        fTreeview = Frame(frame, {"relief": SUNKEN})
        fTreeview.grid_columnconfigure(0, weight=1)
        fTreeview.grid_rowconfigure(0, weight=1)
        fTreeview.grid({"row": 1, "column": 0, "sticky": NSEW})
        self.tree = tv.TreeViewTable(fTreeview, {"CPF": 150, 'Nome': 300, 'Departamento': 150})
        self.tree.appendItem(("287.871.726-87", "Gilberto Cysneiros", "CEINFO"))







