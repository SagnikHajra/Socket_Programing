import tkinter as tk
from tkinter import filedialog, Text, scrolledtext
import os

master = tk.Tk()
master.title("Welcome to Client")
master.geometry('700x700')

master.wm_attributes("-transparentcolor", "yellow")

frame1 = tk.Frame(master=master, width=400, height=100, bg="yellow")
frame1.wm_attributes("-transparentcolor", "yellow")
frame1.pack()

frame2 = tk.Frame(master=master, width=400, height=100, bg="yellow")
frame2.wm_attributes("-transparentcolor", "yellow")
frame2.pack()

frame3 = tk.Frame(master=master, width=600, height=400, bg="yellow")
frame3.wm_attributes("-transparentcolor", "yellow")
frame3.pack()


def addFile():
    filename = filedialog.askopenfilename(initialdir="/", title="select file",
                                          filetypes=(("text", "*.txt",), ("all files", "*.*",))
                                          )


def submit_entry_fields():
    pass

# tk.Label(master, text="First Name").grid(row=0)
# tk.Label(master, text="Last Name").grid(row=1)
#
# e1 = tk.Entry(master)
# e2 = tk.Entry(master)
#
# e1.grid(row=0, column=1)
# e2.grid(row=1, column=1)
#


# tk.Button(master, text='Quit', command=master.quit).grid(row=1, column=20, sticky=tk.W, pady=4)
# tk.Button(master, text='Connect', command=submit_entry_fields).grid(row=3, column=1, sticky=tk.W, pady=4)




# openFile = tk.Button(master, text="Open File", padx=10, pady=5, fg="black", bg='lightgrey', command=addFile)
# openFile.pack()

master.mainloop()

# root = tk.Tk()
#
#
# def addFile():
#     filename = filedialog.askopenfilename(initialdir="/", title="select file",
#                                           filetypes=(("text", "*.txt",), ("all files", "*.*",))
#                                           )
# #root.wm_attributes("-transparentcolor", "yellow")
#
#
# tk.Label(root, text="        Server").grid(row=0)
# tk.Label(root, text="Address").grid(row=1)
# tk.Label(root, text="Port").grid(row=2)
#
# e1 = tk.Entry(root)
# e2 = tk.Entry(root)
# e3 = tk.Entry(root)
#
# e3.grid(row=0, column=1)
# e1.grid(row=1, column=1)
# e2.grid(row=2, column=1)
#
#
# openFile = tk.Button(root, text="Open File", padx=10, pady=5, fg="black", bg='lightgrey', command=addFile)
# openFile.pack()
# root.mainloop()
