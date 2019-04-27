
from tkinter import *
from tkinter import ttk


class Gui:
    def __init__(self):
        self.root = Tk()
        self.root.config({"width": 500, "height": 400})
        self.root.title("Projeto CRUD II - Controle Acadêmico Simplificado")
        self.center_window(self.root)

        self.do_login()
        self.root.mainloop()

    def do_login(self):

        # Disable main window
        self.root.wm_attributes("-disabled", True)

        # Create the login dialog
        self.login_dialog = Toplevel(self.root)
        self.login_dialog.config({"width": 300, "height": 200})

        # Tell the window manager, this is the child widget.
        # Interesting, if you want to let the child window
        # flash if user clicks onto parent
        self.login_dialog.transient(self.root)

        # This is watching the window manager close button
        # and uses the same callback function as the other buttons
        # (you can use which ever you want, BUT REMEMBER TO ENABLE
        # THE PARENT WINDOW AGAIN)
        self.login_dialog.protocol("WM_DELETE_WINDOW", self.close_login_dialog)

        self.center_window(self.login_dialog)
        self.loginF = Frame(self.login_dialog, {"bg": "yellow"})
        self.loginF.place({"relx": .5, "rely": .5, "anchor": CENTER})
        Label(self.loginF, {"text": "Login:", "bg": "yellow"}).grid({"row": 0, "column": 0, "padx": 10, "pady": 10})
        login = StringVar()
        Entry(self.loginF, {"textvariable": login}).grid({"row": 0, "column": 1, "padx": 10, "pady": 10})
        Label(self.loginF, {"text": "Senha:", "bg": "yellow"}).grid({"row": 1, "column": 0, "padx": 10, "pady": 10})
        Entry(self.loginF).grid({"row": 1, "column": 1, "padx": 10, "pady": 10})
        Button(self.loginF, {"text": "Logar", "width": 10, "command": self.close_login_dialog}).grid({"row": 2, "column": 0, "columnspan": 2, "pady": 10})
        self.login_dialog.mainloop()

    def center_window(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def close_login_dialog(self):
        # IMPORTANT!
        self.root.wm_attributes("-disabled", False)  # IMPORTANT! Enable main window

        self.login_dialog.destroy()

        # Possibly not needed, used to focus parent window again
        self.root.deiconify()


if __name__ == '__main__':
    gui = Gui()




