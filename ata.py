
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

        mainF = Frame(self)
        mainF.grid({"row": 0, "column": 0, "sticky": NSEW, "pady": 2, "padx": 2})
        mainF.grid_rowconfigure(0, weight=1)
        mainF.grid_rowconfigure(1, weight=1)
        mainF.grid_columnconfigure(0, weight=1)

        topF = Frame(mainF, padx=8, pady=8, borderwidth=1, relief='groove', background='white')
        topF.grid({"row": 0, "column": 0, "sticky": NSEW})
        topF.grid_rowconfigure(0, weight=1)
        topF.grid_columnconfigure(0, weight=0)
        topF.grid_columnconfigure(1, weight=1)
        topLeftF = Frame(topF, background='white')
        topLeftF.grid(row=0, column=0, sticky=NSEW)
        HeaderLeft(topLeftF)

        topRightF = Frame(topF, bg='white')
        topRightF.grid(row=0, column=1, sticky=NSEW)
        topRightF.grid_columnconfigure(0, weight=1)
        header_right = HeaderRight(topRightF)

        bottomF = Frame(mainF, padx=8, pady=8)
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

        header_right.preencher_turma(id_turma)
        self._listar_alunos(id_turma)

    def _listar_alunos(self, id_turma):
        query = '''SELECT cpf, name FROM students WHERE id IN
                   (SELECT student_id FROM class_students WHERE class_id = {})
                   ORDER BY name ASC'''.format(id_turma)
        order = 1
        for student in Sqlite.db_conn.cursor.execute(query):
            student = list(student)
            student[0] = ~tools.CPF(student[0])
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


class HeaderRight(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.configure(background='white')
        self.grid(row=0, column=0, sticky=NSEW)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        Label(self,
              text='CÓDIGO DA DISCIPLINA',
              font=('bold', 8),
              anchor=W).grid(row=0, column=0, sticky=EW)
        Label(self,
              text='PERÍODO',
              font=('bold', 8)).grid(row=0, column=1, sticky=EW)
        Label(self,
              text='TURMA',
              font=('bold', 8)).grid(row=0, column=2, sticky=EW)
        self.subjectcode = StringVar()
        Label(self,
              textvariable=self.subjectcode,
              font=('bold', 8),
              background='white',
              bd=1,
              relief=GROOVE).grid(row=1, column=0, sticky=EW)
        self.period = StringVar()
        Label(self,
              textvariable=self.period,
              font=('bold', 8),
              background='white',
              bd=1,
              relief=GROOVE).grid(row=1, column=1, sticky=EW)
        self.classcode = StringVar()
        Label(self,
              textvariable=self.classcode,
              font=('bold', 8),
              background='white',
              bd=1,
              relief=GROOVE).grid(row=1, column=2, sticky=EW)

        Label(self,
              text='NOME DA DISCIPLINA',
              font=('bold', 8),
              anchor=W).grid(row=2, column=0, columnspan=3, sticky=EW)
        self.subjectname = StringVar()
        Label(self,
              textvariable=self.subjectname,
              font=('bold', 8),
              background='white',
              bd=1,
              relief=GROOVE).grid(row=3, column=0, columnspan=3, sticky=EW)

        Label(self,
              text='PROFESSOR(ES)',
              font=('bold', 8),
              anchor=W).grid(row=4, column=0, columnspan=3, sticky=EW)
        self.profs = Listbox(self, height=3)
        self.profs.grid(row=5, column=0, columnspan=3, sticky=EW)

    def preencher_turma(self, id_turma):
        # update GUI top right form with class infos
        query = '''SELECT classes.code, classes.semester, subjects.code, subjects.name
                   FROM classes LEFT JOIN subjects ON classes.subject = subjects.id
                   WHERE classes.id = {}'''.format(id_turma)
        Sqlite.db_conn.cursor.execute(query)
        res = Sqlite.db_conn.cursor.fetchone()
        self.classcode.set(res[0])
        self.period.set(res[1])
        self.subjectcode.set(res[2])
        self.subjectname.set(res[3].upper())
        # fill in top right listbox with profs
        query = '''SELECT professors.name FROM class_professors
                   LEFT JOIN professors ON class_professors.professor_id = professors.id
                   WHERE class_professors.class_id = {} ORDER BY professors.name ASC'''.format(id_turma)
        for res in Sqlite.db_conn.cursor.execute(query):
            self.profs.insert(END, res[0].upper())















