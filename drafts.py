from tkinter import *
import tkinter.ttk as ttk


'''class FancyListbox(tkinter.Listbox):

    def __init__(self, parent, *args, **kwargs):
        tkinter.Listbox.__init__(self, parent, *args, **kwargs)

        self.popup_menu = tkinter.Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Delete",
                                    command=self.delete_selected)
        self.popup_menu.add_command(label="Select All",
                                    command=self.select_all)

        self.bind("<Button-3>", self.popup) # Button-2 on Aqua

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def delete_selected(self):
        for i in self.curselection()[::-1]:
            self.delete(i)

    def select_all(self):
        self.selection_set(0, 'end')
'''


class TreeViewTable(ttk.Treeview):
    def __init__(self, parent, headers):
        colnames = list(headers.keys())
        colwidths = list(headers.values())
        super(TreeViewTable, self).__init__(parent, columns=colnames[1:], selectmode='extended')
        self.grid({"row": 0, "column": 0, "sticky": NSEW})
        # insere cabeçalhos e define suas larguras
        for ix, header in enumerate(colnames):
            self.heading("#{}".format(ix), text=header)
            self.column("#{}".format(ix), minwidth=colwidths[ix], width=colwidths[ix], stretch=NO)

    def appendItem(self, data, pos='', iid=None):
        self.insert(pos, 'end', iid, text=data[0], values=data[1:])

    def get_selection(self):
        selection = self.selection()
        ret = []
        for iid in selection:
            dict = self.item(iid)      # lê dados da seleção em dicionário
            dict.update({'iid': iid})       # acrescenta id (chave primária) da seleção
            ret.append(dict)
        return ret


root = Tk()
'''flb = FancyListbox(root, selectmode='multiple')
for n in range(10):
    flb.insert('end', n)
flb.pack()'''
tv = TreeViewTable(root, {"Código": 150, "Disciplina": 450})
tv.appendItem(('06234', 'Matemática Discreta'))
tv.appendItem(('06203', 'Teoria Geral da Administração'))
print(tv.get_selection())
root.mainloop()



