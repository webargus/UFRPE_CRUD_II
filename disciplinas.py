

from tkinter import *
import treeviewtable as tv
import tools


class PainelDisciplinas:

    def __init__(self, frame):

        frame.grid_rowconfigure(0, weight=0)    # 0 => row won't expand vertically if there's space for that
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # cria frame p/ formulário de cadastro de disciplinas
        fDiscip = LabelFrame(frame, {"pady": 8, "padx": 8, "text": " Cadastro "})
        fDiscip.grid({"row": 0, "column": 0, "sticky": NSEW, "pady": 8, "padx": 8})
        fDiscip.grid_columnconfigure(1, weight=1)    # expande formulário na horizontal até bordas da janela
        Label(fDiscip, {"text": "Disciplina:"}).grid({"row": 0, "column": 0})
        self.nome = StringVar()
        self.nomeEdit = Entry(fDiscip, {"textvariable": self.nome}).grid({"row": 0, "column": 1, "columnspan": 3, "sticky": (W, E)})
        Label(fDiscip, {"text": "Código:"}).grid({"row": 1, "column": 0, "sticky": W})
        self.codigo = StringVar()
        self.codigoEdit = Entry(fDiscip, {"textvariable": self.codigo}).grid({"row": 1, "column": 1, "sticky": W})
        self.submitBtn = Button(fDiscip, {"text": "Ok", "width": 10, "command": self._salvar_disciplina}).grid({"row": 1, "column": 2, "pady": 8})
        self.delBtn = Button(fDiscip, {"text": "Excluir", "width": 10}).grid({"row": 1, "column": 3, "pady": 8, "padx": 8})

        fTreeview = Frame(frame, {"relief": SUNKEN})
        fTreeview.grid_columnconfigure(0, weight=1)
        fTreeview.grid_rowconfigure(0, weight=1)
        fTreeview.grid({"row": 1, "column": 0, "sticky": NSEW})
        self.tree = tv.TreeViewTable(fTreeview, {"Código": 150, 'Disciplina': 600})
        self.tree.appendItem(("04166", "Teoria Geral da Administração"))

    def _salvar_disciplina(self):
        # valida entrada da disciplina e retorna se inválida
        v = self._validar_disc()
        if v is None:
            return
        # verifica se código já inserido anteriormente
        query = "SELECT * FROM subjects WHERE code = '%s'" % (v[0])
        print(query)


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





