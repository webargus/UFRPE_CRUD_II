

from tkinter import *
import treeviewtable as tv


class PainelDisciplinas:

    def __init__(self, frame):

        frame.grid_rowconfigure(0, weight=0)    # 0 => row won't expand vertically if there's space for that
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # cria frame p/ formulário de cadastro de disciplinas
        fDiscip = LabelFrame(frame, {"pady": 8, "padx": 8, "text": " Cadastro "})
        fDiscip.grid({"row": 0, "column": 0, "sticky": NSEW, "pady": 8, "padx": 8})
        fDiscip.grid_columnconfigure(1, weight=1)    # expande formulário na horizontal até bordas da janela
        Label(fDiscip, {"text": "Disciplina:"}).grid({"row": 0, "column": 0})
        self.nomeEdit = Entry(fDiscip).grid({"row": 0, "column": 1, "columnspan": 3, "sticky": (W, E)})
        Label(fDiscip, {"text": "Código:"}).grid({"row": 1, "column": 0, "sticky": W})
        self.codigoEdit = Entry(fDiscip).grid({"row": 1, "column": 1, "sticky": W})
        self.submitBtn = Button(fDiscip, {"text": "Ok", "width": 10}).grid({"row": 1, "column": 2, "pady": 8})
        self.delBtn = Button(fDiscip, {"text": "Excluir", "width": 10}).grid({"row": 1, "column": 3, "pady": 8, "padx": 8})

        fTreeview = Frame(frame, {"relief": SUNKEN})
        fTreeview.grid_columnconfigure(0, weight=1)
        fTreeview.grid_rowconfigure(0, weight=1)
        fTreeview.grid({"row": 1, "column": 0, "sticky": NSEW})
        self.tree = tv.TreeViewTable(fTreeview, {"Código": 150, 'Disciplina': 600})
        self.tree.appendItem(("04166", "Teoria Geral da Administração"))







