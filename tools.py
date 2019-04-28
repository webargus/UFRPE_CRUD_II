

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














