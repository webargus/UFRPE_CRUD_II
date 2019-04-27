
from tkinter import *
from tkinter import ttk


class Gui:

    def __init__(self):
        self.root = Tk()
        self.root.wm_minsize(800, 600)
        self.root.state('normal')
        self.root.title("Projeto CRUD II - Controle Acadêmico Simplificado")
        center_window(self.root)

        self.do_login()
        self.root.mainloop()

    def do_login(self):

        # Disable main window
        self.root.wm_attributes("-disabled", True)

        # Create the login dialog
        self.login_dialog = Toplevel(self.root, {"bg": "yellow"})
        self.login_dialog.config({"width": 300, "height": 200})
        self.login_dialog.after(500, lambda: self.login_dialog.focus_force())

        # Tell the window manager, this is the child widget.
        # Interesting, if you want to let the child window
        # flash if user clicks onto parent
        self.login_dialog.transient(self.root)

        # This is watching the window manager close button
        # and uses the same callback function as the other buttons
        # (you can use which ever you want, BUT REMEMBER TO ENABLE
        # THE PARENT WINDOW AGAIN)
        # self.login_dialog.protocol("WM_DELETE_WINDOW", self.close_login_dialog)
        self.login_dialog.protocol("WM_DELETE_WINDOW", self.close_login_dialog)

        center_window(self.login_dialog)
        self.loginF = Frame(self.login_dialog, {"bg": "yellow"})
        self.loginF.place({"relx": .5, "rely": .5, "anchor": CENTER})
        Label(self.loginF, {"text": "Login:", "bg": "yellow"}).grid({"row": 0, "column": 0, "padx": 10, "pady": 10})
        login = StringVar()
        Entry(self.loginF, {"textvariable": login}).grid({"row": 0, "column": 1, "padx": 10, "pady": 10})
        Label(self.loginF, {"text": "Senha:", "bg": "yellow"}).grid({"row": 1, "column": 0, "padx": 10, "pady": 10})
        Entry(self.loginF).grid({"row": 1, "column": 1, "padx": 10, "pady": 10})
        Button(self.loginF, {"text": "Logar", "width": 10, "command": self.process_login}).grid({"row": 2, "column": 0, "columnspan": 2, "pady": 10})
        self.login_dialog.mainloop()

    def close_login_dialog(self):
        # destroy both, login and main windows if user clicked on login quit button (quit program)
        self.login_dialog.destroy()
        self.root.destroy()

    def process_login(self):

        self.root.wm_attributes("-disabled", False)     # IMPORTANT! enable main window
        self.login_dialog.destroy()


def center_window(win):
    # call update_idletasks before retrieving any geometry,
    # to ensure that the values returned are accurate
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    # print("width=%d; height=%d; x=%d; y=%d" % (width, height, x, y))


if __name__ == '__main__':
    gui = Gui()




