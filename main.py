
from tkinter import *
from tkinter.ttk import *
import sqltools
import tools
import disciplinas
import professores
import alunos
import login


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
        f1 = Frame(n)   # frame p/ disciplinas
        f2 = Frame(n)   # frame p/ professores
        f3 = Frame(n)   # frame p/ alunos
        #   acrescenta abas
        n.add(f1, text='Disciplinas')
        n.add(f2, text='Professores')
        n.add(f3, text='Alunos')
        n.grid({"row": 0, "column": 0, "sticky": NSEW})

        pdiscip = disciplinas.PainelDisciplinas(f1)
        pdiscip.listar_disciplinas()
        pprofs = professores.PainelProfessores(f2)
        palunos = alunos.PainelAlunos(f3)

        # login.LoginDialog(self)
        self.mainloop()


if __name__ == '__main__':
    gui = Gui()




