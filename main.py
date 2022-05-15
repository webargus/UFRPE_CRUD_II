
from tkinter import *
from tkinter.ttk import *
import sqltools
import tools
import disciplinas
import professores
import alunos
import turmas
import login


class Gui(Frame):

    db_conn = sqltools.Sqlite()

    def __init__(self):
        Frame.__init__(self)
        # self.master.iconbitmap(tools.icon32)
        tools.StaticImages()
        self.master.wm_minsize(1200, 600)
        self.master.state('normal')
        self.master.title("Projeto CRUD II - Controle Acadêmico Simplificado")
        tools.center_window(self.master)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        #   self.master.grid_columnconfigure(1, weight=1)  # there's NO column 1 in master!!
        self.grid({"row": 0, "column": 0, "sticky": NSEW})
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        #   self.grid_columnconfigure(1, weight=1)         # theres's NO column 1 in parent!!

        n = Notebook(self)
        f1 = Frame(n)   # frame p/ disciplinas
        f2 = Frame(n)   # frame p/ professores
        f3 = Frame(n)   # frame p/ alunos
        #   acrescenta abas
        n.add(f1, text='Disciplinas')
        n.add(f2, text='Professores')
        n.add(f3, text='Alunos')
        n.grid({"row": 0, "column": 0, "sticky": NSEW})

        frame = Frame(self, relief=SUNKEN, borderwidth=1)
        frame.grid({"row": 0, "column": 1, "sticky": NSEW, "pady": 2, "padx": 2})
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.turmas = turmas.Turmas(frame)

        pdiscip = disciplinas.PainelDisciplinas(f1, self.turmas)
        pdiscip.listar_disciplinas()
        prof_panel = professores.PainelProfessores(f2, self.turmas)
        self.turmas.append_callback(prof_panel.listar_professores)
        alunos.PainelAlunos(f3, self.turmas)

        # login.LoginDialog(self)
        self.mainloop()


if __name__ == '__main__':
    gui = Gui()




