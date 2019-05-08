import tkinter as TK

class MyApp(TK.Frame):

    def __init__(self, master):
        super().__init__(master) # initialize the 'TK.Frame'

        # configure the root Frame (i.e. 'self')
        self.master = master # just for reference later
        self.master.grid_rowconfigure(0, weight = 1)
        self.master.grid_columnconfigure(0, weight = 1)
        self.grid(column = 0, row = 0, sticky = 'nsew')
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1) # columns will split space
        self.grid_columnconfigure(1, weight = 1) # columns will split space

        # configure internal left Frame
        self.left_frame = TK.Frame(self, borderwidth = 2, relief = TK.SUNKEN)
        self.left_frame.grid_rowconfigure(0, weight = 1) # rows will split space
        self.left_frame.grid_rowconfigure(1, weight = 1) # rows will split space
        self.left_frame.grid_columnconfigure(0, weight = 1)
        self.left_frame.grid(column = 0, row = 0, sticky = 'nsew')
        self.left_box0 = TK.Listbox(self.left_frame, borderwidth = 0)
        self.left_box0.grid(column = 0, row = 0, sticky = 'nsew')
        self.left_box1 = TK.Listbox(self.left_frame, borderwidth = 0)
        self.left_box1.grid(column = 0, row = 1, sticky = 'nsew')

        # configure internal right Frame
        self.right_frame = TK.Frame(self, borderwidth = 2, relief = TK.SUNKEN)
        self.right_frame.grid_rowconfigure(0, weight = 1) # rows will split space
        self.right_frame.grid_rowconfigure(1, weight = 1) # rows will split space
        self.right_frame.grid_columnconfigure(0, weight = 1)
        self.right_frame.grid(column = 1, row = 0, sticky = 'nsew')
        self.right_box0 = TK.Listbox(self.right_frame, borderwidth = 0)
        self.right_box0.grid(column = 0, row = 0, sticky = 'nsew')
        self.right_box1 = TK.Listbox(self.right_frame, borderwidth = 0)
        self.right_box1.grid(column = 0, row = 1, sticky = 'nsew')

        for i in range(20):
            self.left_box0.insert(TK.END, 'lb0')
            self.left_box1.insert(TK.END, 'lb1')
            self.right_box0.insert(TK.END, 'rb0')
            self.right_box1.insert(TK.END, 'rb1')


if __name__ == '__main__': # get in the habit of doing this
    root = TK.Tk()
    root.title('My App')
    root.geometry('{}x{}'.format(768, 500))
    root.resizable(width = False, height = False)
    app = MyApp(root)
    app.mainloop()

