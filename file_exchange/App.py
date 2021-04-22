import tkinter as tk
from tkinter import filedialog, Text, scrolledtext as st
import os.path
from SocketFunc import SocketClass

closeSocket = False
socket = fileName = None

address = "localhost"
port = "9000"
username = 'abc'

titleFont = ("Arial", 12)
subTitleFont = ("Arial", 10)
buttonPadx = 5
buttonPady = 0.5

master = tk.Tk()
master.title("Welcome to Client")
master.geometry('800x800')
queue = []
#backgroundColor = "#60b26c"
backgroundColor = "black"

# master.wm_attributes("-transparentcolor", backgroundColor)


# Used by multiple functions to maintain state of the buttons
def changeState(buttonName):
    if buttonName["state"] == tk.NORMAL:
        buttonName.config(state=tk.DISABLED)
    else:
        buttonName.config(state=tk.NORMAL)


# When user press {Add File} button this func is execute
def addFile():
    global fileName
    fileName = filedialog.askopenfilename(initialdir="/", title="select file",
                                          filetypes=(("text", "*.txt",), ("all files", "*.*",)))
    fileLabel.config(text=f"File Name: {fileName}")

    changeState(sendFile)


def insert(msg):
    textArea.insert(tk.INSERT, "> " + msg + '\n')


# When Server sends Close Conn request this function is executed from local function receive()
def closeConn():
    global fileName
    insert("Closing the client socket...")
    socket.socket.close()
    insert("client socket is closed...")
    changeState(connButton)
    changeState(openFile)
    changeState(sendFile)
    fileName = ''
    fileLabel.config(text="")


# Sends the file to the server after {Send} button is pressed
def sendFile():
    global fileName
    if not fileName or not os.path.isfile(fileName):
        insert("filename is blank or filePath doesn't exist")
        return

    file = open(fileName, 'r').read()

    if send(file):
        while True:
            flag, serverMsg = receive()
            if not flag and serverMsg not in socket.messages:
                insert(serverMsg)
                xy = open(f'{fileName}.converted', 'w')
                xy.write(serverMsg)
                xy.close()
            else:
                break


# Calls the  SocketClass function receive() and listen to the server, then passes that to the source
def receive():
    while True:
        try:
            serverMsg = socket.receive(socket.socket)
        except ConnectionResetError as e:
            insert(e.strerror)
            return False, ''
        if serverMsg in (socket.WELCOME, socket.USER_VERIFIED):
            insert(socket.messages[serverMsg])
        elif serverMsg in (socket.USERNAME, socket.FILE,):
            insert(socket.messages[serverMsg])
            return True, serverMsg
        elif serverMsg == socket.CONNECTION_CLOSE:
            insert(socket.messages[serverMsg])
            closeConn()
            return False, serverMsg
        elif serverMsg == socket.USER_INVALID:
            insert(socket.messages[serverMsg])
            return False, serverMsg
        elif serverMsg == socket.POOL:
            return True, serverMsg
        else:
            return False, serverMsg


# Sends message recevd from console to SocketClass function send()
def send(msg):
    try:
        socket.send(msg, socket.socket)
    except (ConnectionRefusedError, ConnectionResetError) as e:
        insert(e.strerror)
        return False
    return True


def checkQueueAndSend():
    if queue.len() > 0:
        listToStr = ' '.join(map(str, queue))
        insert(listToStr)
        send(listToStr)


# Estbl connection with server after recving address/Port via input boxes
def connectionHandler():
    global socket, address, port
    address = E1.get()
    port = E2.get()
    try:
        socket = SocketClass(address, int(port))
    except (ConnectionRefusedError, ConnectionResetError) as e:
        insert(e.strerror)
        return
    flag, serverMsg = receive()
    if flag:
        if serverMsg == socket.USERNAME:
            changeState(submit)
            changeState(connButton)
            return
        elif serverMsg == socket.POOL:
            insert("Got poll")
            checkQueueAndSend()
    elif serverMsg == socket.CONNECTION_CLOSE:
        return
    insert(f"Error: unexpected message received"
           f"[{socket.messages[serverMsg] if serverMsg in socket.messages else serverMsg}]"
           )

def addToQueue():
    addedWord = E35.get()
    E35.delete(0, 'end')
    queue.append(addedWord)
    queueArea.insert(tk.INSERT, addedWord + '\n')



# Submits the Username
def submitHandler():
    global username
    username = E31.get()
    insert(username)
    if username.strip():
        if send(username):
            flag, serverMsg = receive()
            if flag:
                if serverMsg == socket.FILE:
                    changeState(submit)
                    changeState(openFile)
                    return
            elif serverMsg in (socket.USER_INVALID, socket.CONNECTION_CLOSE):
                return
            insert(f"Error: unexpected message received"
                   f"[{socket.messages[serverMsg] if serverMsg in socket.messages else serverMsg}]"
                   )
        else:
            changeState(submit)
            changeState(connButton)
    else:
        insert(f"Please be cool and type something")

# ###############  FRAME1[Server Info]  ############################
# Frame2 has {Server} title label, {Address} and {Port} input boxes and {Connect} button
# #####################################################
frame1 = tk.Frame(master=master, width=600, height=110, bg=backgroundColor)

tk.Label(
    frame1, text="Server", font=titleFont, bg=backgroundColor, fg="bisque", justify="center").place(x=250, y=1)

tk.Label(
    frame1, text="Address : ", font=subTitleFont, bg=backgroundColor, fg="bisque", justify="center").place(x=190, y=22)
add = tk.StringVar(frame1, value=address)
E1 = tk.Entry(
    frame1, textvariable=add, font=subTitleFont, bg="lightgrey", fg="black", cursor="xterm black"
)
E1.place(x=250, y=22)

tk.Label(
    frame1, text="Port :", font=subTitleFont, bg=backgroundColor, fg="bisque", justify="center").place(x=190, y=45)
prt = tk.StringVar(frame1, value=port)
E2 = tk.Entry(
    frame1, textvariable=prt, font=subTitleFont, bg="lightgrey", fg="black", cursor="xterm black"
)
E2.place(x=250, y=45)
connButton = tk.Button(
    frame1, text="Connect", command=connectionHandler, state=tk.NORMAL, font=subTitleFont,
                       bg=backgroundColor, fg="bisque", pady=buttonPady, padx=buttonPadx)
connButton.place(x=250, y=68)

# frame1.wm_attributes("-transparentcolor", backgroundColor)
frame1.pack()

# ###############  FRAME2[Username]  ############################
# Frame2 only has {Username} input box and {Submit} button
# #####################################################
frame2 = tk.Frame(master=master, width=600, height=30, bg=backgroundColor)

tk.Label(frame2, text="Username: ", font=subTitleFont, bg=backgroundColor, fg="bisque", justify="center").place(x=150, y=2)

user = tk.StringVar(frame2, value=username)
E31 = tk.Entry(
    frame2, textvariable=user, font=subTitleFont, bg="lightgrey", fg="black", cursor="xterm black")

E31.place(x=235, y=2)
submit = tk.Button(master=frame2, text="Submit", font=subTitleFont, bg=backgroundColor, fg="bisque",
                   state=tk.DISABLED, command=submitHandler)
submit.place(x=400, y=0)
frame2.pack()

# ###############  FRAME3[File Upload]  #############################################
# Frame2 has {Open File} button, added {File Name} label and {Send} to server button
# all under header {Upload a Text file}
# ###################################################################################
frame3 = tk.Frame(master=master, width=600, height=122, bg=backgroundColor)
# frame3.wm_attributes("-transparentcolor", backgroundColor)

tk.Label(frame3, text="Upload a text file", font=titleFont, bg=backgroundColor, fg="bisque", justify="center").place(x=220,
                                                                                                               y=0)
openFile = tk.Button(frame3, text="Open File", state=tk.DISABLED, padx=buttonPadx, pady=buttonPady, bg=backgroundColor,
                     fg="bisque", justify="center", command=addFile)
openFile.place(x=250, y=22)
# The below label is kept blank intentionally and shows the file path when user selects a file using {Open File} button
fileLabel = tk.Label(frame3, text="", font=("Cambria", 8), bg=backgroundColor, fg="bisque", justify="center")
fileLabel.place(x=150, y=50)

sendFile = tk.Button(frame3, text="Send", state=tk.DISABLED, font=subTitleFont, padx=buttonPadx, pady=buttonPady,
                     bg=backgroundColor, fg="bisque", justify="center", command=sendFile)
sendFile.place(x=260, y=70)
textLabel = tk.Label(master=frame3, text="Console Log", font=("Arial", 12), bg=backgroundColor, fg="bisque").place(x=240,
                                                                                                             y=100)
frame3.pack()

# ###############  FRAME4  ############################
# Frame4 only has input box and {add} button
# #####################################################
frame4 = tk.Frame(master=master, width=600, height=30, bg=backgroundColor)

E35 = tk.Entry(frame4, font=subTitleFont, bg="lightgrey", fg="black", cursor="xterm black")
E35.place(x=235, y=2)

add = tk.Button(master=frame4, text="add", font=subTitleFont, bg=backgroundColor, fg="bisque", command=addToQueue)
add.place(x=400, y=0)
frame4.pack()

# ############# Scrollable #############################
# Scrollable Console Log for Log information
# #######################################################
textArea = st.ScrolledText(master=master, bg=backgroundColor, fg="bisque", padx=10, pady=5, font=("Courier", 12), height=15)
textArea.pack()

# ############# Scrollable #############################
# Scrollable Console Log for queue values.
# #######################################################
queueArea = st.ScrolledText(master=master, bg=backgroundColor, fg="bisque", padx=5, pady=5, font=("Courier", 12), height=15)
queueArea.pack()


# ################## Exit button ###########################
tk.Button(master, text='Exit', command=master.quit, font=("Arial", 10), bg="grey", fg="bisque", pady=.8, padx=10).pack(
    side="bottom")
# ############### Keep the window on top always #################
# master.call('wm', 'attributes', '.', '-topmost', True)
master.mainloop()
