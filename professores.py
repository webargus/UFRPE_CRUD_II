

from tkinter import *
import treeviewtable as tv
import tools
from sqltools import Sqlite


class PainelProfessores:

    def __init__(self, frame, turmas):

        # hold ref to 'turmas' panel
        self.turmas = turmas

        frame.grid_rowconfigure(0, weight=0)    # 0 => row won't expand vertically if there's space for that
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # cria frame p/ formulário de cadastro de professor
        fProf = LabelFrame(frame, {"pady": 8, "padx": 8, "text": " Cadastro "})
        fProf.grid({"row": 0, "column": 0, "sticky": NSEW, "pady": 8, "padx": 8})
        fProf.grid_columnconfigure(4, weight=1)    # expande formulário na horizontal até bordas da janela
        Label(fProf, {"text": "Nome:"}).grid({"row": 0, "column": 0})
        self.nome = StringVar()
        Entry(fProf, {"textvariable": self.nome}).grid({"row": 0, "column": 1, "columnspan": 5, "sticky": (W, E)})
        Label(fProf, {"text": "CPF:"}).grid({"row": 1, "column": 0, "sticky": W})
        self.cpf = StringVar()
        Entry(fProf, {"textvariable": self.cpf}).grid({"row": 1, "column": 1, "sticky": W})
        Label(fProf, {"text": "Departamento:"}).grid({"row": 1, "column": 2, "sticky": W, "padx": 4})
        self.depto = StringVar()
        Entry(fProf, {"width": 30, "textvariable": self.depto}).grid({"row": 1, "column": 3, "sticky": W})
        params = {"text": "Ok",
                  "width": 70,
                  "image": tools.StaticImages.tick16,
                  "compound": "left",
                  "command": self._salvar_professor
                  }
        Button(fProf, params).grid({"row": 1, "column": 4, "padx": 4, "pady": 8, "sticky": E})
        params = {"text": "Excluir",
                  "width": 70,
                  "image": tools.StaticImages.del16,
                  "compound": "left"
                  }
        Button(fProf, params).grid({"row": 1, "column": 5, "pady": 8, "sticky": E})

        fTreeview = Frame(frame, {"relief": SUNKEN})
        fTreeview.grid_columnconfigure(0, weight=1)
        fTreeview.grid_rowconfigure(0, weight=1)
        fTreeview.grid({"row": 1, "column": 0, "sticky": NSEW})
        self.tree = tv.TreeViewTable(fTreeview, {"CPF": 150, 'Nome': 300, 'Departamento': 150})
        self.tree.on_select(self._selecionar_professor)
        self.tree.on_mouse_right(self._popup)

        self.popup_menu = Menu(frame, tearoff=0, bd=4)
        self.popup_menu.add_command(label="Adicionar", command=self._set_prof_turma)

        self.listar_professores()

    def _popup(self, event):
        sel = self.tree.get_selection()
        if len(sel) == 0:
            return
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def _set_prof_turma(self):
        sel = self.tree.get_selection()
        param = []
        for s in sel:
            if self.tree.parent(s['iid']):
                continue
            param.append({'id': s['iid'],
                          'cpf': s['text'],
                          'nome': s['values'][0],
                          'depto': s['values'][1]
                          }
                         )
        self.turmas.set_professores(param)

    def _salvar_professor(self):
        # valida entrada do professor e retorna se inválida
        v = self._validar_professor()
        if v is None:
            return
        # verifica se CPF já inserido anteriormente
        query = "SELECT * FROM professors WHERE cpf = '%s'" % (v[0])
        Sqlite.db_conn.cursor.execute(query)
        res = Sqlite.db_conn.cursor.fetchone()
        # print(res)    # debug
        if res is None:     # CPF not found in db => operation is of type INSERT
            query = "INSERT INTO professors (cpf, name, department) VALUES('%s', '%s', '%s')" % (v[0], v[1], v[2])
        else:               # code already exists in db => operation is of type UPDATE
            query = "UPDATE professors SET name = '%s', department = '%s' WHERE professors.id = %s" % (v[1], v[2], res[0])
        Sqlite.db_conn.cursor.execute(query)
        Sqlite.db_conn.conn.commit()
        self.listar_professores()
        self.turmas.listar_turmas()

    def _validar_professor(self):
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
        depto = self.depto.get().strip()
        if len(depto) == 0:
            erros.append("Departamento em branco")
        if len(erros) > 0:
            tools.aviso_erro(erros)
            return None
        return [cpf, nome, depto]

    def listar_professores(self):
        self.tree.clear()     # clear tree view
        query = "SELECT * FROM professors ORDER BY name"
        query1 = '''SELECT classes.code, subjects.code, subjects.name, semester, class_id FROM class_professors
                    LEFT JOIN classes ON class_id = classes.id
                    LEFT JOIN subjects ON subjects.id = classes.subject
                    WHERE professor_id = {}
                    ORDER BY semester, subjects.name ASC'''
        Sqlite.db_conn.cursor.execute(query)
        profs = Sqlite.db_conn.cursor.fetchall()
        for row in profs:
            # append professor to tree view
            self.tree.appendItem(row[1:], iid=row[0])
            # query for professor classes from db
            Sqlite.db_conn.cursor.execute(query1.format(row[0]))
            turmas = Sqlite.db_conn.cursor.fetchall()
            for turma in turmas:
                turma = list(turma)
                turma = [str(x) for x in turma]
                class_id = turma.pop()
                semester = turma.pop()
                semester_id = str(row[0]) + "." + semester
                if not self.tree.exists(semester_id):
                    self.tree.appendItem([semester], pos=row[0], iid=semester_id)
                # assign unique string id to child id;
                # string id = parent id = professor PK (iid) + hyphen + class primary key (class_id)
                str_id = str(row[0]) + "-" + str(class_id)
                if self.tree.exists(str_id):
                    continue
                # print("turma=", turma)    # debug
                turma = turma[0:1] + [' - '.join(turma[1:])]
                self.tree.appendItem(turma, pos=semester_id, iid=str_id)

    def _selecionar_professor(self, items):
        #   print(items)    #   debug
        if (len(items) > 1) or self.tree.parent(items[0]['iid']):
            self._set_professor(('', '', ''))
            return
        self._set_professor((items[0]['text'], items[0]['values'][0], items[0]['values'][1]))

    def _set_professor(self, tupla):
        self.cpf.set(tupla[0])
        self.nome.set(tupla[1])
        self.depto.set(tupla[2])










