import tkinter as tk
from tkinter import filedialog, Text, scrolledtext
import os.path
from SocketFunc import SocketClass

closeSocket = False
socket = fileName = None

address = "localhost"
port = "9000"


def addFile():
    filename = filedialog.askopenfilename(initialdir="/", title="select file",
                                          filetypes=(("text", "*.txt",), ("all files", "*.*",))
                                          )


master = tk.Tk()
master.title("Welcome to Client")
# master.geometry('700x700')

master.wm_attributes("-transparentcolor", "#60b26c")


def changeState(buttonName):
    if buttonName["state"] == tk.NORMAL:
        buttonName.config(state=tk.DISABLED)
    else:
        buttonName.config(state=tk.NORMAL)


def addFile():
    global fileName
    fileName = filedialog.askopenfilename(initialdir="/", title="select file",
                                          filetypes=(("text", "*.txt",), ("all files", "*.*",)))
    fileLabel.config(text=f"File Name: {fileName}")
    changeState(sendFile)


def sendFile():
    changeState(connButton)
    changeState(openFile)
    changeState(sendFile)
    fileLabel.config(text="")
    pass


def submit_entry_fields():
    global socket, address, port
    address = E1.get()
    port = E2.get()
    socket = SocketClass(address, int(port))

    changeState(connButton)
    changeState(openFile)


frame1 = tk.Frame(master=master, width=600, height=150, bg="#60b26c")

tk.Label(frame1, text="Server", font=("Arial bold", 16), bg="#60b26c", fg="white", justify="center").place(x=250, y=1)

tk.Label(frame1, text="Address : ", font=("Arial", 10), bg="#60b26c", fg="white", justify="center").place(x=190, y=40)
add = tk.StringVar(frame1, value=address)
E1 = tk.Entry(frame1, textvariable=add, font=("Arial", 10), bg="lightgrey", fg="black", cursor="xterm black black")
E1.place(x=250, y=40)

tk.Label(frame1, text="Port :", font=("Arial", 10), bg="#60b26c", fg="white", justify="center").place(x=190, y=60)
prt = tk.StringVar(frame1, value=port)
E2 = tk.Entry(frame1, textvariable=prt, font=("Arial", 10), bg="lightgrey", fg="black", cursor="xterm black black")
E2.place(x=250, y=60)

connButton = tk.Button(frame1, text="Connect", command=submit_entry_fields, state=tk.NORMAL, font=("Arial", 10),
                       bg="#60b26c", fg="white", pady=.8, padx=10)
connButton.place(x=250, y=90)

frame1.wm_attributes("-transparentcolor", "#60b26c")
frame1.pack()




frame2 = tk.Frame(master=master, width=600, height=150, bg="#60b26c")
frame2.wm_attributes("-transparentcolor", "#60b26c")

tk.Label(frame2, text="Upload a text file", font=("Arial", 14), bg="#60b26c", fg="white", justify="center").place(x=220,
                                                                                                                  y=1)
openFile = tk.Button(frame2, text="Open File", state=tk.DISABLED, padx=10, pady=.8, bg="#60b26c", fg="white", justify="center", command=addFile)
openFile.place(x=250, y=30)
fileLabel = tk.Label(frame2, text="", font=("Cambria", 8), bg="#60b26c", fg="white", justify="center")
fileLabel.place(x=150, y=60)
sendFile = tk.Button(frame2, text="Send", state=tk.DISABLED, padx=10, pady=.8, bg="#60b26c", fg="white", justify="center", command=sendFile)
sendFile.place(x=260, y=90)

frame2.pack()




frame3 = tk.Frame(master=master, width=600, height=400, bg="#60b26c")
frame3.wm_attributes("-transparentcolor", "#60b26c")
frame3.pack()




tk.Button(master, text='Quit', command=master.quit, font=("Arial", 10), bg="grey", fg="white", pady=.8, padx=10).pack(
    side="bottom")

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
master.call('wm', 'attributes', '.', '-topmost', True)
master.mainloop()

# root = tk.Tk()
#
#
# def addFile():
#     filename = filedialog.askopenfilename(initialdir="/", title="select file",
#                                           filetypes=(("text", "*.txt",), ("all files", "*.*",))
#                                           )
# #root.wm_attributes("-transparentcolor", "#60b26c")
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
