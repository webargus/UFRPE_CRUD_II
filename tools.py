import re
import tkinter
from tkinter import messagebox

cpf_pattern1 = r"^\d{11}$"              # expressões regulares para validar CPF
# cpf_pattern2 = r"^(\d{3}\.){2}\d{3}-\d{2}$"
disciplina_pattern = r"^\d{5}$"         # expressão regular para validar código de disciplina
periodo_pattern = r"^\d{4}\.\d{1}$"     # expressão regular para validar período de turma

img_path = "C:\\Users\\Edson\\PycharmProjects\\UFRPE_CRUD_II\\img\\"
icon32 = img_path + "brasao32.ico"
tick16 = img_path+"tick.png"
new16 = img_path + "plus16.png"
shield = img_path + "brasao1.png"


class StaticImages:

    def __init__(self):
        StaticImages.tick16 = tkinter.PhotoImage(file=tick16)
        StaticImages.new16 = tkinter.PhotoImage(file=new16)
        StaticImages.shield = tkinter.PhotoImage(file=shield)


def center_window(win):
    # call update_idletasks before retrieving any geometry,
    # to ensure that the values returned are accurate
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    # print("width=%d; height=%d; x=%d; y=%d" % (width, height, x, y))  # debug


def validar_disciplina(codigo):
    #   verifica se o código da disciplina consiste em string de 5 algarismos
    if re.match(disciplina_pattern, codigo) is None:
        return False
    return True


def validar_periodo(periodo):
    #   verifica se o periodo está no formato aaaa.s, p.ex., 2019.1, 2018.2
    if re.match(periodo_pattern, periodo) is None:
        return False
    return True


def validar_cpf(cpf):
    #   Função para validar CPF; retorna True se CPF válido, False se não válido
    if re.match(cpf_pattern1, cpf) is None:
        return False
    return True


def formatar_cpf(cpf):
    #   retorna string de CPF no formato xxx.xxx.xxx-xx
    ret = ''        # string acumuladora do CPF formatado
    for x in range(0, 9, 3):        # acrescenta '.' a cada 3 algarismos
        ret += cpf[x:x+3] + '.'
    ret = ret[:-1]                  # descarta o último '.' acrescentado e
    ret += '-' + cpf[-2:]           # substitui por um '-' seguido dos 2 últimos algarismos
    return ret


def desformatar_cpf(cpf):
    ret = cpf.replace('.', '')
    ret = ret.replace('-', '')
    return ret


class CPFStringVar(tkinter.StringVar):
    def __init__(self):
        super().__init__()

    def set(self, v):
        v = formatar_cpf(v)
        super().set(v)

    def get(self):
        v = super().get()
        v = desformatar_cpf(v)
        return v


def aviso_erro(erros):
    msg = "Favor verificar:\n"
    messagebox.showwarning("...Êpa!!", (msg + "\n".join(erros)))

def aviso_cancelar_ok(msg):
    return messagebox.askokcancel("Atenção!!", msg)











