from tkinter import *
import treeviewtable as tv
import tools
from sqltools import Sqlite


class Turmas:

    def __init__(self, parent):

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
        listbox = ProfessorListbox(fprofs)
        listbox.grid({"row": 0, "column": 0, "sticky": EW})
        Button(fprofs, {"text": "X", "padx": 4}).grid({"row": 0, "column": 1, "padx": 4})

        # form ok/delete buttons
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

        fbottom = Frame(frame)
        # make row 0 of fbottom extend vertically to take up the whole vertical space available
        # in parent Frame row (row 1 of frame obj)
        fbottom.grid_rowconfigure(0, weight=1)
        # tells parent Frame obj (== frame) that fbottom goes inside cell (row=1, col=0) of frame obj
        fbottom.grid({"row": 1, "column": 0, "sticky": NSEW})

        self.tree = tv.TreeViewTable(fbottom, {"Código": 50, "Período": 100, "Código Disciplina": 70, "Disciplina": 300})

    def set_disciplina(self, discip):
        #   print(discip)   #   debug
        self.discip.set_disciplina(discip)

    def _salvar_turma(self):
        turma = self._validar_turma()
        if turma is None:
            return
        print(turma)        # debug

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
        disciplina = self.discip.get_id_disciplina()
        if disciplina is None:
            erros.append("Disciplina em branco")

        if len(erros) > 0:
            tools.aviso_erro(erros)
            return None
        return [codigo, periodo, disciplina]


class ProfessorListbox(Listbox):

    def __init__(self, parent):
        super().__init__(parent, {"height": 3})


class DisciplinaLabel(Label):

    def __init__(self, parent):
        self.discip = None
        self.label = StringVar()
        super().__init__(parent, {"relief": SUNKEN, "textvariable": self.label})

    def set_disciplina(self, discip):
        self.discip = discip
        self.label.set(discip[0]['text'] + ' - ' + discip[0]['values'][0])
        print(self.discip)      #   debug

    def get_id_disciplina(self):
        if self.discip is None:
            return None
        return self.discip[0]['iid']










