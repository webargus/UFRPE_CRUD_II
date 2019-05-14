

from tkinter import *
import treeviewtable as tv
import tools

class PainelAlunos:

    def __init__(self, frame):

        frame.grid_rowconfigure(0, weight=0)    # 0 => row won't expand vertically if there's space for that
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # cria frame p/ formulário de cadastro de aluno
        fAluno = LabelFrame(frame, {"pady": 8, "padx": 8, "text": " Cadastro "})
        fAluno.grid({"row": 0, "column": 0, "sticky": NSEW, "pady": 8, "padx": 8})
        fAluno.grid_columnconfigure(1, weight=1)    # expande formulário na horizontal até bordas da janela
        Label(fAluno, {"text": "Nome:"}).grid({"row": 0, "column": 0})
        Entry(fAluno).grid({"row": 0, "column": 1, "columnspan": 3, "sticky": (W, E)})
        Label(fAluno, {"text": "CPF:"}).grid({"row": 1, "column": 0, "sticky": W})
        Entry(fAluno).grid({"row": 1, "column": 1, "sticky": W})
        params = {"text": "Ok",
                  "width": 70,
                  "image": tools.StaticImages.tick16,
                  "compound": "left"
                  }
        Button(fAluno, params).grid({"row": 1, "column": 2, "pady": 8})
        params = {"text": "Excluir",
                  "width": 70,
                  "image": tools.StaticImages.del16,
                  "compound": "left"
                  }
        Button(fAluno, params).grid({"row": 1, "column": 3, "pady": 8, "padx": 8})

        fTreeview = Frame(frame, {"relief": SUNKEN})
        fTreeview.grid_columnconfigure(0, weight=1)
        fTreeview.grid_rowconfigure(0, weight=1)
        fTreeview.grid({"row": 1, "column": 0, "sticky": NSEW})
        self.tree = tv.TreeViewTable(fTreeview, {"CPF": 150, 'Nome': 450})










