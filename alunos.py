
from tkinter import *
import treeviewtable as tv
import tools
from sqltools import Sqlite


class PainelAlunos:

    def __init__(self, frame, turmas):

        self.turmas = turmas

        frame.grid_rowconfigure(0, weight=0)    # 0 => row won't expand vertically if there's space for that
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # cria frame p/ formulário de cadastro de aluno
        fAluno = LabelFrame(frame, {"pady": 8, "padx": 8, "text": " Cadastro "})
        fAluno.grid({"row": 0, "column": 0, "sticky": NSEW, "pady": 8, "padx": 8})
        fAluno.grid_columnconfigure(1, weight=1)    # expande formulário na horizontal até bordas da janela
        Label(fAluno, {"text": "Nome:"}).grid({"row": 0, "column": 0})
        self.nome = StringVar()
        Entry(fAluno, {"textvariable": self.nome}).grid({"row": 0, "column": 1, "columnspan": 2, "sticky": (W, E)})
        Label(fAluno, {"text": "CPF:"}).grid({"row": 1, "column": 0, "sticky": W})
        self.cpf = StringVar()
        Entry(fAluno, {"textvariable": self.cpf}).grid({"row": 1, "column": 1, "sticky": W})
        params = {"text": "Ok",
                  "width": 70,
                  "image": tools.StaticImages.tick16,
                  "compound": "left",
                  "command": self._salvar_aluno
                  }
        Button(fAluno, params).grid({"row": 1, "column": 2, "pady": 8})
        '''params = {"text": "Excluir",
                  "width": 70,
                  "image": tools.StaticImages.del16,
                  "compound": "left"
                  }
        Button(fAluno, params).grid({"row": 1, "column": 3, "pady": 8, "padx": 8})'''

        fTreeview = Frame(frame, {"relief": SUNKEN})
        fTreeview.grid_columnconfigure(0, weight=1)
        fTreeview.grid_rowconfigure(0, weight=1)
        fTreeview.grid({"row": 1, "column": 0, "sticky": NSEW})
        self.tree = tv.TreeViewTable(fTreeview, {"CPF": 150, 'Nome': 450})
        self.tree.on_select(self._selecionar_aluno)
        self.tree.on_mouse_right(self._popup)

        self.popup_menu = Menu(frame, tearoff=0, bd=4)
        self.popup_menu.add_command(label="Matricular aluno(s)", command=self._set_alunos_turma)
        self.popup_menu.add_command(label="Cancelar matrícula(s)", command=self._cancelar_matriculas)
        self.popup_menu.add_command(label="Excluir aluno(s)", command=self._excluir_alunos)

        self.turmas.append_callback(self.listar_alunos)
        self.listar_alunos()

    def _popup(self, event):
        sel = len(self.tree.get_selection())
        if sel == 0:
            return
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def _excluir_alunos(self):
        sel = self.tree.get_selection()
        # get only selected students
        sel = [x for x in sel if not self.tree.parent(x['iid'])]
        if len(sel) == 0:
            return
        s = ""
        for aluno in sel:
            s += aluno['text'] + ' - ' + ' - '.join([str(y) for y in aluno['values']]) + "\n"
        if not tools.aviso_cancelar_ok(s + "\nConfirma a exclusão desse(s) aluno(s)?"):
            return
        sel = ', '.join([x['iid'] for x in sel])
        query = '''DELETE FROM students WHERE id IN ({})'''.format(sel)
        Sqlite.db_conn.cursor.execute(query)
        query = '''DELETE FROM class_students WHERE student_id IN ({})'''.format(sel)
        Sqlite.db_conn.cursor.execute(query)
        Sqlite.db_conn.conn.commit()
        self.listar_alunos()

    def _cancelar_matriculas(self):
        # get selected classes only
        sel = self.tree.get_selection()
        # get ids for which there are no children == ids of classes,
        # and delete them from tree view
        sel = [x['iid'] for x in sel if len(self.tree.get_children(x['iid'])) == 0]
        for id in sel:
            self.tree.delete(id)
        # wipe out childless branches from tree view
        childless = [y for x in self.tree.get_children() for y in self.tree.get_children(x) if len(self.tree.get_children(y)) == 0]
        # print("childless=", childless)    # debug
        for child in childless:
            self.tree.delete(child)
        # and split them into sublists where pos = 0 corresponds to student id and
        # pos = 1 corresponds to class id
        sel = [x.split('-') for x in sel]
        self.turmas.remover_matriculas(sel)

    def _set_alunos_turma(self):
        # get selected parents only (students, though)
        sel = self.tree.get_selection()
        # sift through parents for student ids
        ids = [s['iid'] for s in sel if not self.tree.parent(s['iid'])]
        # call turma module 'set_alunos' method to assign students to classes
        # (eventually) selected in 'turmas' panel tree view;
        # the turma.set_alunos method returns ids of classes assigned to students
        turma_ids = self.turmas.set_alunos(ids)
        query = '''SELECT classes.code, subjects.code, subjects.name, classes.semester, classes.id
                   FROM classes LEFT JOIN subjects ON classes.subject = subjects.id
                   WHERE classes.id IN ({})'''.format(', '.join(turma_ids))
        Sqlite.db_conn.cursor.execute(query)
        turmas = Sqlite.db_conn.cursor.fetchall()
        # loop over student ids (iid) seeking to append tree view branch with their classes
        for iid in ids:
            for turma in turmas:
                turma = list(turma)
                class_id = turma.pop()
                semester = turma.pop()
                semester_id = str(iid) + "." + semester
                if not self.tree.exists(semester_id):
                    self.tree.appendItem([semester], pos=iid, iid=semester_id)
                # assign unique string id to child id;
                # string id = parent id = student PK (iid) + hyphen + class primary key (class_id)
                str_id = str(iid) + "-" + str(class_id)
                if self.tree.exists(str_id):
                    continue
                turma = turma[0:1] + [' - '.join(turma[1:])]
                self.tree.appendItem(turma, pos=semester_id, iid=str_id)

    def _salvar_aluno(self):
        # valida entrada do aluno e retorna se inválida
        v = self._validar_aluno()
        if v is None:
            return
        # verifica se CPF já inserido anteriormente
        query = "SELECT * FROM students WHERE cpf = '%s'" % (v[0])
        Sqlite.db_conn.cursor.execute(query)
        res = Sqlite.db_conn.cursor.fetchone()
        # print(res)        # debug
        if res is None:     # CPF not found in db => operation is of type INSERT
            query = "INSERT INTO students (cpf, name) VALUES('%s', '%s')" % (v[0], v[1])
        else:               # code already exists in db => operation is of type UPDATE
            query = "UPDATE students SET name = '%s' WHERE id = %s" % (v[1], res[0])
        Sqlite.db_conn.cursor.execute(query)
        Sqlite.db_conn.conn.commit()
        self.listar_alunos()
        self.turmas.listar_turmas()

    def _validar_aluno(self):
        erros = []
        cpf = self.cpf.get().strip()
        cpf = cpf.replace('.', '')
        cpf = cpf.replace('-', '')
        if len(cpf) == 0:
            erros.append("CPF em branco")
        elif not tools.validar_cpf(cpf):
            erros.append("CPF inválido")
        nome = self.nome.get().strip()
        if len(nome) == 0:
            erros.append("Nome do professor em branco")

        if len(erros) > 0:
            tools.aviso_erro(erros)
            return None
        return [cpf, nome]

    def listar_alunos(self):
        self.tree.clear()     # clear tree view
        query = "SELECT * FROM students ORDER BY name"
        students = Sqlite.db_conn.cursor.execute(query).fetchall()
        for row in students:
            self.tree.appendItem(row[1:], iid=row[0])
            # get ids of classes in which student is enrolled
            # REM: do left join just to make sure we retrieve classes sorted by semester in ascending order
            query = '''SELECT class_students.class_id FROM class_students
                       LEFT JOIN classes ON class_students.class_id = classes.id
                       WHERE student_id = {} ORDER BY classes.semester ASC'''.format(row[0])
            student_classes = Sqlite.db_conn.cursor.execute(query).fetchall()
            for class_id in student_classes:
                # get class details
                query = '''SELECT classes.code, subjects.code, subjects.name, classes.semester
                           FROM classes LEFT JOIN subjects ON classes.subject = subjects.id
                           WHERE classes.id = {}'''.format(class_id[0])
                classes = Sqlite.db_conn.cursor.execute(query).fetchall()
                for turma in classes:
                    turma = [str(x) for x in turma]
                    semester = turma.pop()
                    semester_id = str(row[0]) + "." + semester
                    if not self.tree.exists(semester_id):
                        self.tree.appendItem([semester], pos=row[0], iid=semester_id)
                    str_id = str(row[0]) + "-" + str(class_id[0])
                    turma = turma[0:1] + [' - '.join(turma[1:])]
                    self.tree.appendItem(turma, pos=semester_id, iid=str_id)

    def _selecionar_aluno(self, items):
        # print(items)    #   debug
        if (len(items) > 1) or self.tree.parent(items[0]['iid']):
            self._set_aluno(('', ''))
            return
        self._set_aluno((items[0]['text'], items[0]['values'][0]))

    def _set_aluno(self, tupla):
        self.cpf.set(tupla[0])
        self.nome.set(tupla[1])










