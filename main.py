
from tkinter import *
import sqltools
import tools
from tkinter.ttk import *


class Gui(Frame):

    db_conn = sqltools.Sqlite()

    def __init__(self):
        Frame.__init__(self)
        self.master.wm_minsize(800, 600)
        self.master.state('normal')
        self.master.title("Projeto CRUD II - Controle Acadêmico Simplificado")
        tools.center_window(self.master)
        self.pack({"expand": YES, "fill": BOTH, "side": LEFT})
        n = Notebook(self)
        f1 = Frame(n)  # first page, which would get widgets gridded into it
        f2 = Frame(n)  # second page
        n.add(f1, text='One')
        n.add(f2, text='Two')
        n.pack({"expand": YES, "fill": BOTH, "side": LEFT})

        colors = ['red', 'green', 'orange', 'white', 'yellow', 'blue']
        r = 0
        for c in colors:
            Label(f1, text=c, width=25).grid(row=r, column=0)
            Entry(f1).grid(row=r, column=1)
            r = r + 1

        tree = Treeview(f2, columns=('name'))
        tree.bind('<<TreeviewSelect>>', lambda e: print(tree.item(tree.focus())))
        tree.grid({"row": 0, "column": 0})
        tree.heading('#0', text='CPF')
        tree.heading('name', text='Nome')
        img = PhotoImage(file='checkbox_1.png')
        tree.insert('', 'end', text='278.700.814-34', image=img, values=('"Edson Kropniczki"'))
        tree.insert('', 'end', text='button', tags=('ttk', 'simple'))
        tree.tag_configure('ttk', background='yellow', image=img)

        #login.LoginDialog(self)
        self.mainloop()


if __name__ == '__main__':
    gui = Gui()




