import re
import tkinter
from tkinter import messagebox

disciplina_pattern = r"^\d{5}$"         # expressão regular para validar código de disciplina
periodo_pattern = r"^\d{4}\.\d{1}$"     # expressão regular para validar período de turma

# img_path = "C:\\Users\\Edson\\PycharmProjects\\UFRPE_CRUD_II\\img\\"
img_path = "/home/kropniczki/UFRPE/UFRPE_CRUD_II/img/"
icon32 = img_path + "brasao32.ico"
tick16 = img_path+"tick.png"
new16 = img_path + "plus16.png"
shield = img_path + "brasao.png"


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


class CPF(str):

    cpf_pattern = r"^\d{11}$"  # expressão regular para validar CPF

    def __new__(cls, *args, **kw):
        args = list(args)
        args[0] = args[0].replace('.', '')
        args[0] = args[0].replace('-', '')
        return str.__new__(cls, *args, **kw)

    def __invert__(self):
        if not self.valid():
            return ''
        #   retorna string de CPF no formato xxx.xxx.xxx-xx
        ret = ''  # string acumuladora do CPF formatado
        for x in range(0, 9, 3):  # acrescenta '.' a cada 3 algarismos
            ret += self[x:x + 3] + '.'
        ret = ret[:-1]  # descarta o último '.' acrescentado e
        ret += '-' + self[-2:]  # substitui por um '-' seguido dos 2 últimos algarismos
        return ret

    def valid(self):
        #   Função para validar CPF; retorna True se CPF válido, False se não válido
        if re.match(CPF.cpf_pattern, self) is None:
            return False
        return True


def aviso_erro(erros):
    msg = "Favor verificar:\n"
    messagebox.showwarning("...Êpa!!", (msg + "\n".join(erros)))

def aviso_cancelar_ok(msg):
    return messagebox.askokcancel("Atenção!!", msg)











