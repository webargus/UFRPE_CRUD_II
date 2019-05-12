import re
import tkinter
from tkinter import messagebox

cpf_pattern = r"^\d{11}$"               # expressão regular para validar CPF
disciplina_pattern = r"^\d{5}$"         # expressão regular para validar código de disciplina
periodo_pattern = r"^\d{4}\.\d{1}$"     # expressão regular para validar período de turma

img_path = "C:\\Users\\Edson\\PycharmProjects\\UFRPE_CRUD_II\\img\\"
icon32 = img_path + "brasao32.ico"
tick16 = img_path+"tick.png"
delete16 = img_path + "delete16.png"
arrow16 = img_path + "arrow16.png"


class StaticImages:

    def __init__(self):
        StaticImages.tick16 = tkinter.PhotoImage(file=tick16)
        StaticImages.del16 = tkinter.PhotoImage(file=delete16)
        StaticImages.arrow16 = tkinter.PhotoImage(file=arrow16)


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


def aviso_erro(erros):
    msg = "Favor verificar:\n"
    messagebox.showwarning("...Êpa!!", (msg + "\n".join(erros)))













