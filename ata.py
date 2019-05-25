
from tkinter import *
import tools
import labeltable as table
from sqltools import Sqlite

class Ata(Toplevel):

    def __init__(self, parent, id_turma):
        Toplevel.__init__(self, parent.master)
        self.parent = parent
        self.iconbitmap(tools.icon32)
        self.config({"width": 800, "height": 500})
        self.resizable(False, False)
        tools.center_window(self)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        mainF = Frame(self)
        mainF.grid({"row": 0, "column": 0, "sticky": NSEW, "pady": 2, "padx": 2})
        mainF.grid_rowconfigure(0, weight=1)
        mainF.grid_rowconfigure(1, weight=1)
        mainF.grid_columnconfigure(0, weight=1)

        topF = Frame(mainF, relief=SUNKEN, borderwidth=5)
        topF.grid({"row": 0, "column": 0, "sticky": NSEW})
        topF.grid_rowconfigure(0, weight=1)
        topF.grid_columnconfigure(0, weight=1)
        Label(topF, text="provisory label").grid({"row": 0, "column": 0, "sticky": NSEW})

        bottomF = Frame(mainF)
        bottomF.grid({"row": 1, "column": 0, "sticky": NSEW})
        bottomF.grid_rowconfigure(0, weight=1)
        bottomF.grid_columnconfigure(0, weight=1)
        headers = {"ORD": (5, "center"),
                   "Nota": (8, "center"),
                   "CPF": (17, "center"),
                   "Nome do(a) aluno(a)": (39, "w"),
                   "Assinatura": (39, "center")}
        self.table = table.LabelTable(self, headers)
        self.table.cell_config(0, 2, {"anchor": "center"})

        parent.master.wm_attributes("-disabled", True)
        self.after(500, lambda: self.focus_force())
        self.transient(parent.master)
        self.protocol("WM_DELETE_WINDOW", self.__close)

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














