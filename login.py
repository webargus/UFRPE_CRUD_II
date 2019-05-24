
from tkinter import *
import tools


class LoginDialog(Toplevel):

    def __init__(self, parent):
        Toplevel.__init__(self, parent.master, {"bg": "yellow"})
        self.iconbitmap(tools.icon32)
        self.parent = parent
        self.config({"width": 300, "height": 200})
        self.resizable(False, False)
        tools.center_window(self)

        parent.master.wm_attributes("-disabled", True)
        self.after(500, lambda: self.focus_force())
        self.transient(parent.master)
        self.protocol("WM_DELETE_WINDOW", self.__close)

        loginF = Frame(self, {"bg": "yellow"})
        loginF.place({"relx": .5, "rely": .5, "anchor": CENTER})
        self.notify = StringVar()
        Label(loginF, {"textvariable": self.notify, "bg": "yellow"}).grid({"row": 0, "column": 0, "columnspan": 2, "pady": 10})
        self.notify.set("Entre seu login e sua senha:")
        Label(loginF, {"text": "Login:", "bg": "yellow"}).grid({"row": 1, "column": 0, "padx": 10, "pady": 10})
        login = Entry(loginF)
        login.grid({"row": 1, "column": 1, "padx": 10, "pady": 10})
        Label(loginF, {"text": "Senha:", "bg": "yellow"}).grid({"row": 2, "column": 0, "padx": 10, "pady": 10})
        pwd = Entry(loginF, {"show": "*"})
        pwd.grid({"row": 2, "column": 1, "padx": 10, "pady": 10})
        Button(loginF,
               {"text": "Logar", "width": 10, "command": lambda: self.__login(login.get(), pwd.get())}).grid(
            {"row": 3, "column": 0, "columnspan": 2, "pady": 10})
        self.mainloop()

    def __login(self, username, password):
        if self.parent.db_conn.login(username, password) is None:
            self.notify.set("Login e/ou senha inválidos")
            return
        # IMPORTANT! enable main window
        self.parent.master.wm_attributes("-disabled", False)
        self.destroy()

    def __close(self):
        self.destroy()
        self.parent.master.destroy()

