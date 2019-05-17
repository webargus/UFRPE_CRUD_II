
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
        Entry(fAluno, {"textvariable": self.nome}).grid({"row": 0, "column": 1, "columnspan": 3, "sticky": (W, E)})
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
        params = {"text": "Excluir",
                  "width": 70,
                  "image": tools.StaticImages.del16,
                  "compound": "left"
                  }
        Button(fAluno, params).grid({"row": 1, "column": 3, "pady": 8, "padx": 8})

        fTreeview = Frame(frame, {"relief": SUNKEN})
        fTreeview.grid_columnconfigure(0, weight=1)
        fTreeview.grid_rowconfigure(0, weight=1)
        fTreeview.grid({"row": 1, "column": 0, "sticky": NSEW})
        self.tree = tv.TreeViewTable(fTreeview, {"CPF": 150, 'Nome': 450})
        self.tree.on_select(self._selecionar_aluno)
        self.tree.on_mouse_right(self._popup)

        self.popup_menu = Menu(frame, tearoff=0, bd=4)
        self.popup_menu.add_command(label="Adicionar", command=self._set_alunos_turma)

        self.listar_alunos()

    def _popup(self, event):
        sel = len(self.tree.get_selection())
        if sel == 0:
            return
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def _set_alunos_turma(self):
        sel = self.tree.get_selection()
        ids = [s['iid'] for s in sel]
        turma_ids = self.turmas.set_alunos(ids)
        query = '''SELECT classes.code, classes.semester, subjects.name  
                   FROM classes LEFT JOIN subjects ON classes.subject = subjects.id
                   WHERE classes.id IN (''' + ', '.join(turma_ids) + ")"
        Sqlite.db_conn.cursor.execute(query)
        turmas = Sqlite.db_conn.cursor.fetchall()
        for iid in ids:
            for turma in turmas:
                # self.tree.insert(iid, 'end', None, text=turma)
                turma = list(turma[0:1]) + [' - '.join(list(turma[1:]))]
                self.tree.appendItem(turma, pos=iid)

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
        for row in Sqlite.db_conn.cursor.execute(query):
            self.tree.appendItem(row[1:], iid=row[0])

    def _selecionar_aluno(self, items):
        #   print(items)    #   debug
        if len(items) > 1:
            self._set_aluno(('', ''))
            return
        self._set_aluno((items[0]['text'], items[0]['values'][0]))

    def _set_aluno(self, tupla):
        self.cpf.set(tupla[0])
        self.nome.set(tupla[1])










