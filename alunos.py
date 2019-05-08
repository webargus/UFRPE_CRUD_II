

from tkinter import *
import treeviewtable as tv


class PainelAlunos:

    def __init__(self, frame):

        frame.grid_rowconfigure(0, weight=0)    # 0 => row won't expand vertically if there's space for that
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # cria frame p/ formulário de novo aluno
        fAluno = LabelFrame(frame, {"pady": 8, "padx": 8, "text": " Cadastro "})
        fAluno.grid({"row": 0, "column": 0, "sticky": NSEW, "pady": 8, "padx": 8})
        fAluno.grid_columnconfigure(1, weight=1)
        Label(fAluno, {"text": "Nome:"}).grid({"row": 0, "column": 0})
        self.nomeEdit = Entry(fAluno).grid({"row": 0, "column": 1, "columnspan": 2, "sticky": "we"})
        Label(fAluno, {"text": "CPF:"}).grid({"row": 1, "column": 0, "sticky": W})
        self.cpfEdit = Entry(fAluno).grid({"row": 1, "column": 1, "sticky": W})
        self.submitBtn = Button(fAluno, {"text": "Ok", "width": 10}).grid({"row": 1, "column": 2, "pady": 8})

        fTreeview = Frame(frame, {"relief": SUNKEN})
        fTreeview.grid_columnconfigure(0, weight=1)
        fTreeview.grid_rowconfigure(0, weight=1)
        fTreeview.grid({"row": 1, "column": 0, "sticky": NSEW})
        self.tree = tv.TreeViewTable(fTreeview, ("CPF", 'Aluno', 'Turma'))
        self.tree.appendItem(("278.700.814-34", "Edson Kropniczki", "TGA"))










