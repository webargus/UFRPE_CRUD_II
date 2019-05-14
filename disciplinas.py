

from tkinter import *
from tkinter import Menu
import treeviewtable as tv
import tools
from sqltools import Sqlite


class PainelDisciplinas:

    def __init__(self, frame, turmas):

        # save reference to 'turmas' obj
        self.turmas = turmas

        frame.grid_rowconfigure(0, weight=0)    # 0 => row won't expand vertically if there's space for that
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # cria frame p/ formulário de cadastro de disciplinas
        fDiscip = LabelFrame(frame, {"pady": 8, "padx": 8, "text": " Cadastro "})
        fDiscip.grid({"row": 0, "column": 0, "sticky": NSEW, "pady": 8, "padx": 8})
        fDiscip.grid_columnconfigure(1, weight=1)    # expande formulário na horizontal até bordas do frame
        Label(fDiscip, {"text": "Disciplina:"}).grid({"row": 0, "column": 0})
        self.nome = StringVar()
        Entry(fDiscip, {"textvariable": self.nome}).grid({"row": 0, "column": 1, "columnspan": 3, "sticky": EW})
        Label(fDiscip, {"text": "Código:"}).grid({"row": 1, "column": 0, "sticky": W})
        self.codigo = StringVar()
        Entry(fDiscip, {"textvariable": self.codigo}).grid({"row": 1, "column": 1, "sticky": W})
        Button(fDiscip, {"text": "Ok", "width": 70, "image": tools.StaticImages.tick16, "compound": "left", "command": self._salvar_disciplina}).grid({"row": 1, "column": 2, "pady": 8})
        Button(fDiscip, {"text": "Excluir", "width": 70, "image": tools.StaticImages.del16, "compound": "left"}).grid({"row": 1, "column": 3, "pady": 8, "padx": 8})

        fTreeview = Frame(frame, {"relief": SUNKEN})
        fTreeview.grid_columnconfigure(0, weight=1)
        fTreeview.grid_rowconfigure(0, weight=1)
        fTreeview.grid({"row": 1, "column": 0, "sticky": NSEW})
        self.tree = tv.TreeViewTable(fTreeview, {"Código": 150, 'Disciplina': 450})
        self.tree.on_select(self._selecionar_discip)
        self.tree.on_mouse_right(self._popup)

        self.popup_menu = Menu(frame, tearoff=0, bd=4)
        self.popup_menu.add_command(label="Adicionar", command=self._set_discip_turma)

    def _popup(self, event):
        sel = len(self.tree.get_selection())
        if sel == 0 or sel > 1:
            return
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def _set_discip_turma(self):
        sel = self.tree.get_selection()
        param = {'id': sel[0]['iid'], 'codigo': sel[0]['text'], 'disciplina': sel[0]['values'][0]}
        self.turmas.set_disciplina(param)

    def _salvar_disciplina(self):
        # valida entrada da disciplina e retorna se inválida
        v = self._validar_disc()
        if v is None:
            return
        # verifica se código já inserido anteriormente
        query = "SELECT * FROM subjects WHERE code = '%s'" % (v[0])
        Sqlite.db_conn.cursor.execute(query)
        res = Sqlite.db_conn.cursor.fetchone()
        print(res)
        if res is None:     # code not found in db => operation is of type INSERT
            query = "INSERT INTO subjects (code, name) VALUES('%s', '%s')" % (v[0], v[1])
        else:               # code already exists in db => operation is of type UPDATE
            query = "UPDATE subjects SET name = '%s' WHERE subjects.id = %s" % (v[1], res[0])
        Sqlite.db_conn.cursor.execute(query)
        Sqlite.db_conn.conn.commit()
        self.listar_disciplinas()
        self.turmas.listar_turmas()

    def _validar_disc(self):
        codigo = self.codigo.get().strip()
        erros = []
        if len(codigo) == 0:
            erros.append("Código em branco")
        elif not tools.validar_disciplina(codigo):
            erros.append("Código da disciplina inválido\n(Entre 5 algarismos)")
        nome = self.nome.get().strip()
        if len(nome) == 0:
            erros.append("Disciplina em branco")
        if len(erros) > 0:
            tools.aviso_erro(erros)
            return None
        return [codigo, nome]

    def listar_disciplinas(self):
        self.tree.clear()     # clear tree view
        query = "SELECT * FROM subjects ORDER BY name"
        for row in Sqlite.db_conn.cursor.execute(query):
            self.tree.appendItem(row[1:], iid=row[0])

    def _selecionar_discip(self, items):
        #   print(items)    #   debug
        if len(items) > 1:
            self._set_discip(('', ''))
            return
        self._set_discip((items[0]['text'], items[0]['values'][0]))

    def _set_discip(self, tupla):
        self.codigo.set(tupla[0])
        self.nome.set(tupla[1])




