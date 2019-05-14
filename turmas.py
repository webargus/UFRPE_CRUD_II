from tkinter import *
import treeviewtable as tv
import tools
from sqltools import Sqlite


class Turmas:

    def __init__(self, parent):

        # create Turmas main frame;
        # main frame has 1 column and 2 rows stacked up;
        # the top row gets the class edit/create form,
        # while the one below it gets the 'turmas' treeview;
        # the bottom row expands up and down taking up all vertical space available
        frame = Frame(parent)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=0)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid({"row": 0, "column": 1, "sticky": NSEW, "padx": 4, "pady": 4})

        # top class registry form frame
        ftop = LabelFrame(frame, {"pady": 8, "padx": 8, "text": " Cadastro de Turma "})
        ftop.grid({"row": 0, "column": 0, "sticky": NSEW})

        ''' add class registry form widgets '''

        # add class code label + input
        Label(ftop, {"text": "Código:"}).grid({"row": 0, "column": 0})
        self.codigo = StringVar()
        Entry(ftop, {"width": 4, "textvariable": self.codigo}).grid({"row": 0, "column": 1})

        # add class semester label + input
        Label(ftop, {"text": "Período:"}).grid({"row": 0, "column": 2})
        self.periodo = StringVar()
        Entry(ftop, {"width": 5, "textvariable": self.periodo}).grid({"row": 0, "column": 3})

        # add class subject labels
        Label(ftop, {"text": "Disciplina:"}).grid({"row": 0, "column": 4})
        self.discip = StringVar()
        ftop.grid_columnconfigure(5, weight=1)
        # config = {"relief": SUNKEN, "textvariable": self.discip}
        # method PainelDisciplinas._set_discip_turma calls self.set_disciplina to set this label text
        self.discip = DisciplinaLabel(ftop)
        self.discip.grid({"row": 0, "column": 5, "columnspan": 4, "sticky": EW})

        # professors' frame
        fprofs = LabelFrame(ftop, {"pady": 4, "padx": 4, "text": " Professor(es) "})
        fprofs.grid({"row": 1, "column": 0, "columnspan": 6, "sticky": EW})
        fprofs.grid_columnconfigure(0, weight=1)
        self.listbox = ProfessorListbox(fprofs)
        self.listbox.grid({"row": 0, "column": 0, "sticky": EW})

        # form new/ok/delete buttons
        config = {"text": "Novo",
                  "width": 70,
                  "image": tools.StaticImages.new16,
                  "compound": "left",
                  "command": self._nova_turma
                  }
        Button(ftop, config).grid({"row": 1, "column": 6, "padx": 4})
        config = {"text": "Ok",
                  "width": 70,
                  "image": tools.StaticImages.tick16,
                  "compound": "left",
                  "command": self._salvar_turma
                  }
        Button(ftop, config).grid({"row": 1, "column": 7, "padx": 4})
        config = {"text": "Excluir",
                  "width": 70,
                  "image": tools.StaticImages.del16,
                  "compound": "left"
                  }
        Button(ftop, config).grid({"row": 1, "column": 8})

        # create frame to insert treeview
        fbottom = Frame(frame)
        # make row 0 of fbottom extend vertically to take up the whole vertical space available
        # in parent Frame row (row 1 of frame obj)
        fbottom.grid_rowconfigure(0, weight=1)
        # tells parent Frame obj (== frame) that fbottom goes inside cell (row=1, col=0) of frame obj
        fbottom.grid({"row": 1, "column": 0, "sticky": NSEW})

        self.tree = tv.TreeViewTable(fbottom, {"Código": 50, "Período": 100, "Código Disciplina": 70, "Disciplina": 300})
        self.tree.on_select(self._selecionar_turma)

        self.listar_turmas()

    def set_disciplina(self, discip):
        #   print(discip)   #   debug
        self.discip.set_disciplina(discip)

    def set_professores(self, params):
        self.listbox.append(params)

    def _selecionar_turma(self, items):
        # just clear registry form and abort if user selected more than one 'turma'
        if len(items) > 1:
            self._limpa_formulario_cadastro()
            return
        if len(items) == 0:
            return
        # copy items to form
        # print(items)      # debug
        self.codigo.set(items[0]['text'])
        self.periodo.set(items[0]['values'][0])
        query = '''SELECT subjects.id, subjects.code, subjects.name FROM classes LEFT JOIN subjects
                   ON subjects.id = classes.subject WHERE classes.id = {}'''.format(items[0]['iid'])
        # print("query=", query) # debug
        Sqlite.db_conn.cursor.execute(query)
        row = Sqlite.db_conn.cursor.fetchone()
        param = {'id': row[0], 'codigo': row[1], 'disciplina': row[2]}
        self.discip.set_disciplina(param)
        # read fresh, complete class professor list from db
        query = '''SELECT professor_id FROM class_professors WHERE class_id = {}'''.format(items[0]['iid'])
        Sqlite.db_conn.cursor.execute(query)
        ids = Sqlite.db_conn.cursor.fetchall()
        ids = [str(x[0]) for x in ids]
        query = '''SELECT * FROM professors WHERE id IN ({})'''.format(', '.join(ids))
        Sqlite.db_conn.cursor.execute(query)
        profs = Sqlite.db_conn.cursor.fetchall()
        params = []
        for prof in profs:
            params.append({'id': str(prof[0]), 'cpf': prof[1], 'nome': prof[2], 'depto': prof[3]})
        self.listbox.clear()
        self.listbox.append(params)


    def _nova_turma(self):
        self._limpa_formulario_cadastro()
        self.tree.clear_selection()

    def _limpa_formulario_cadastro(self):
        self.codigo.set('')
        self.periodo.set('')
        self.discip.clear()
        self.listbox.clear()

    def _salvar_turma(self):
        turma = self._validar_turma()
        if turma is None:
            return
        print(turma)        # debug
        if turma['id'] is None:       # insertion operation
            query = '''INSERT INTO classes ('code', 'semester', 'subject')
                       VALUES('{}', '{}', {})
                    '''.format(turma['codigo'], turma['periodo'], turma['disciplina'])
            Sqlite.db_conn.cursor.execute(query)
            turma['id'] = Sqlite.db_conn.cursor.lastrowid
        else:                                   # update op
            query = '''UPDATE classes SET 'code' = '{}', 'semester' = '{}', 'subject' = {}
                       WHERE classes.id = {}'''.format(turma['codigo'],
                                                       turma['periodo'],
                                                       turma['disciplina'],
                                                       turma['id']
                                                       )
            Sqlite.db_conn.cursor.execute(query)

        # update binding table between professors and classes
        query = '''DELETE FROM class_professors WHERE class_id = {}'''.format(turma['id'])
        Sqlite.db_conn.cursor.execute(query)
        # prepare query to bind professors to class
        query = '''INSERT INTO class_professors (class_id, professor_id) VALUES({}, ?)'''.format(turma['id'])
        ids = self.listbox.get_prof_ids()
        for prof_id in ids:
            Sqlite.db_conn.cursor.execute(query, prof_id)
        # commit db transaction
        Sqlite.db_conn.conn.commit()
        self.listar_turmas()

    def listar_turmas(self):
        sel = self.tree.get_selection()
        items = []
        if len(sel) > 0:
            items = [x['iid'] for x in sel]
        self._limpa_formulario_cadastro()
        self.tree.clear()
        query = '''SELECT classes.id, classes.code, classes.semester,
                   subjects.code, subjects.name FROM classes LEFT JOIN subjects
                   ON classes.subject = subjects.id ORDER BY classes.semester ASC'''
        for row in Sqlite.db_conn.cursor.execute(query):
            self.tree.appendItem(row[1:], iid=row[0])

        self.tree.selection_set(items)

    def _validar_turma(self):
        erros = []
        codigo = self.codigo.get().strip()
        if len(codigo) == 0:
            erros.append("Código em branco")
        periodo = self.periodo.get().strip()
        if len(periodo) == 0:
            erros.append("Período em branco")
        elif not tools.validar_periodo(periodo):
            erros.append("Período inválido (formato: aaaa.s, ex.: 2019.1)")
        disciplina = self.discip.get()
        if disciplina is None:
            erros.append("Disciplina em branco")

        if len(erros) > 0:
            tools.aviso_erro(erros)
            return None
        # decide whether we're editing or inserting new turma based on tree view selection;
        # if no selection made or user selected more than one class, they must have started
        # typing in a blank form -> new registry
        sel = self.tree.get_selection()
        if len(sel) == 0 or len(sel) > 1:
            iid = None
        else:
            iid = sel[0]['iid']

        return {'codigo': codigo, 'periodo': periodo, 'disciplina': disciplina, 'id': iid}


class ProfessorListbox(Listbox):

    def __init__(self, parent):
        super().__init__(parent, {"height": 3, "selectmode": EXTENDED})
        self.professors = []
        self.popup_menu = Menu(self, tearoff=0, bd=4)
        self.popup_menu.add_command(label="Excluir", command=self.remove_selected)
        self.bind('<3>', self._popup_menu)

    def _popup_menu(self, event):
        if len(self.curselection()) == 0:
            return
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def append(self, params):
        for prof in params:
            if self.find_prof(prof['id']) is None:
                self.professors.append(prof)
        self.refresh()

    def find_prof(self, prof_id):
        for prof in self.professors:
            if prof['id'] == prof_id:
                return prof
        return None

    def remove_selected(self):
        # get selected indices
        sel = self.curselection()
        # accumulate items to be removed in array according to their indices
        to_remove = []
        for ix, row in enumerate(self.professors):
            if ix in sel:
                to_remove.append(row)
        # actually remove items
        for row in to_remove:
            self.professors.remove(row)
        # refresh listbox
        self.refresh()

    def refresh(self):
        self.delete(0, END)
        for row in self.professors:
            self.insert(END, "%s - %s" % (row['nome'], row['depto']))

    def clear(self):
        self.delete(0, END)     # clear GUI
        del self.professors[:]      # clear professors list

    def get_prof_ids(self):
        return [iid for registry in self.professors for iid in registry['id']]


class DisciplinaLabel(Label):

    def __init__(self, parent):
        self.discip = None
        self.label = StringVar()
        super().__init__(parent, {"relief": SUNKEN, "textvariable": self.label})

    def set_disciplina(self, discip):
        self.discip = discip
        self.label.set(discip['codigo'] + ' - ' + discip['disciplina'])
        # print(self.discip)      # debug

    def get(self):
        if self.discip is None:
            return None
        return self.discip['id']

    def clear(self):
        self.label.set('')
        self.discip = None











