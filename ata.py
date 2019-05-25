
import datetime
from tkinter import *
import labeltable as table
from sqltools import Sqlite
import tools


class Ata(Toplevel):

    def __init__(self, parent, id_turma):
        Toplevel.__init__(self, parent)
        self.parent = parent
        self.iconbitmap(tools.icon32)
        self.config({"width": 800, "height": 500})
        self.resizable(False, False)
        tools.center_window(self)

        parent.master.wm_attributes("-disabled", True)
        self.after(500, lambda: self.focus_force())
        self.transient(parent.master)
        self.protocol("WM_DELETE_WINDOW", self.__close)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.mainF = Frame(self)
        self.mainF.grid({"row": 0, "column": 0, "sticky": NSEW, "pady": 2, "padx": 2})
        self.mainF.grid_rowconfigure(0, weight=1)
        self.mainF.grid_rowconfigure(1, weight=1)
        self.mainF.grid_columnconfigure(0, weight=1)

        self.topF = Frame(self.mainF, padx=8, pady=8, borderwidth=1, relief='groove', background='white')
        self.topF.grid({"row": 0, "column": 0, "sticky": NSEW})
        self.topF.grid_rowconfigure(0, weight=1)
        self.topF.grid_columnconfigure(0, weight=1)
        self.topF.grid_columnconfigure(1, weight=1)
        self.topLeftF = Frame(self.topF, background='white')
        self.topLeftF.grid(row=0, column=0, sticky=NSEW)
        HeaderLeft(self.topLeftF)

        self.topRightF = Frame(self.topF)
        self.topRightF.grid(row=0, column=1, sticky=NSEW)
        Label(self.topRightF, text="Em construção").grid(row=0, column=0, sticky=NSEW)

        bottomF = Frame(self.mainF, padx=8, pady=8)
        bottomF.grid({"row": 1, "column": 0, "sticky": NSEW})
        bottomF.grid_rowconfigure(0, weight=1)
        bottomF.grid_columnconfigure(0, weight=1)
        headers = {"ORD": (5, "center"),
                   "Nota": (8, "center"),
                   "CPF": (17, "center"),
                   "Nome do(a) aluno(a)": (38, "w"),
                   "Assinatura": (38, "center")}
        self.table = table.LabelTable(bottomF, headers)
        self.table.cell_config(0, 2, {"anchor": "center"})

        self._listar_alunos(id_turma)

    def _listar_alunos(self, id_turma):
        query = '''SELECT cpf, name FROM students WHERE id IN
                   (SELECT student_id FROM class_students WHERE class_id = {})
                   ORDER BY name ASC'''.format(id_turma)
        order = 1
        for student in Sqlite.db_conn.cursor.execute(query):
            student = list(student)
            student.append(' ')
            student = [order, ' '] + student
            self.table.insert(student)
            order += 1
            # print(student)    # debug

    def __close(self):
        self.parent.master.wm_attributes("-disabled", False)
        self.destroy()


''' '''


class HeaderLeft(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.configure(background='white')
        self.grid(row=0, column=0, sticky=NSEW)
        Label(self, image=tools.StaticImages.shield, background='white').grid(row=0, column=0, rowspan=5)
        Label(self, text='UNIVERSIDADE FEDERAL RURAL DE\nPERNAMBUCO',
                    font=(None, 14),
                    background='white').grid(row=0, column=1)
        Label(self, text='DEPARTAMENTO DE REGISTRO E CONTROLE ACADÊMICO',
                    font=(None, 10),
                    background='white').grid(row=1, column=1)
        Label(self, text='COORD. DE BACHARELADO EM SISTEMAS DE INFORMAÇÃO', background='white').grid(row=2, column=1)
        Label(self, text='Ata de Presença', font='bold', background='white').grid(row=3, column=1)
        agora = datetime.datetime.now()
        agora = agora.strftime("%d/%m/%y - %H:%M")
        Label(self, text=agora, background='white').grid(row=4, column=1)


















