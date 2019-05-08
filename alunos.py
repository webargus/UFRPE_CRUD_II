

from tkinter import *
import treeviewtable as tv


class PainelAlunos:

    def __init__(self, frame):
        frame.grid_rowconfigure(0, weight=0)    # 0 => row won't expand vertically if there's space for that
        frame.grid_rowconfigure(1, weight=1)
        # cria frame p/ formulário de novo aluno
        fNovoAluno = Frame(frame, {"relief": SUNKEN, "pady": 8, "padx": 8})
        fNovoAluno.grid({"row": 0, "column": 0, "sticky": NSEW})
        fNovoAluno.grid_columnconfigure(1, weight=1)
        Label(fNovoAluno, {"text": "Nome:"}).grid({"row": 0, "column": 0})
        self.nomeEdit = Entry(fNovoAluno).grid({"row": 0, "column": 1, "columnspan": 2, "sticky": "we"})
        Label(fNovoAluno, {"text": "CPF:"}).grid({"row": 1, "column": 0, "sticky": W})
        self.cpfEdit = Entry(fNovoAluno).grid({"row": 1, "column": 1, "sticky": W})
        self.submitBtn = Button(fNovoAluno, {"text": "Ok", "width": 10}).grid({"row": 1, "column": 2, "pady": 8})

        fTreeview = Frame(frame, {"relief": SUNKEN})
        fTreeview.grid({"row": 1, "column": 0, "sticky": NSEW})
        self.tree = tv.TreeViewTable(fTreeview, ("CPF", 'Aluno', 'Turma'))
        self.tree.appendItem(("278.700.814-34", "Edson Kropniczki", "TGA"))










