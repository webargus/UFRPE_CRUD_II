
from tkinter import *
from tkinter.ttk import *
import sqltools
import tools
import treeviewtable as tv
import alunos
#import login


class Gui(Frame):

    db_conn = sqltools.Sqlite()

    def __init__(self):
        Frame.__init__(self)
        self.master.wm_minsize(800, 400)
        self.master.state('normal')
        self.master.title("Projeto CRUD II - Controle Acadêmico Simplificado")
        tools.center_window(self.master)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.grid({"row": 0, "column": 0, "sticky": NSEW})
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        n = Notebook(self)
        f1 = Frame(n)
        '''f1.grid_rowconfigure(0, weight=1)
        f1.grid_columnconfigure(0, weight=1)
        f1.grid({"row": 0, "column": 0, "sticky": NSEW})'''
        f2 = Frame(n)  # second page
        '''f2.grid_rowconfigure(0, weight=1)
        f2.grid_columnconfigure(0, weight=1)
        f2.grid({"row": 0, "column": 0, "sticky": NSEW})'''
        n.add(f1, text='Disciplinas')
        n.add(f2, text='Alunos')
        n.grid({"row": 0, "column": 0, "sticky": NSEW})

        palunos = alunos.PainelAlunos(f1)

        tree = tv.TreeViewTable(f2, ("CPF", 'Aluno', 'Turma'))
        tree.appendItem(("278.700.814-34", "Edson Kropniczki", "TGA"))

        # login.LoginDialog(self)
        self.mainloop()


if __name__ == '__main__':
    gui = Gui()




