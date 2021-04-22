import time

from SocketFunc import SocketClass
# from server import server
import threading
import re
import tkinter as tk
from tkinter import filedialog, Text, scrolledtext as st
import os.path


titleFont = ("Arial", 12)
subTitleFont = ("Arial", 10)
buttonPadx = 5
buttonPady = 0.5

master = tk.Tk()
master.title("Welcome to Server")
master.geometry('600x540')
backgroundColor = "black"
# socket=None

connections = []

with open('words.txt','r') as f:
    print("Words file opened")
    for line in f:
        wordList = line.split(" ")
        wordDict = {x.strip() for x in wordList}
    print("Dictionary is ", wordDict)


userTable = set()
DELAY_TIME = 0.1


def check_every_sixty_seconds(n=60):
    while True:
        for eachClient in connections:
            socket.send(socket.POOL, eachClient, DELAY_TIME)
        time.sleep(n)


def insert(msg):
    textArea.insert(tk.INSERT, "> " + msg + '\n')


def verifyUsername(clientSocket, counter=0):
    if counter > 3:
        return False, ''
    username = socket.receive(clientSocket)
    if username in userTable:
        socket.send(socket.USER_INVALID, clientSocket, DELAY_TIME)
        verified = verifyUsername(clientSocket, counter+1)
    else:
        verified = True
        userTable.add(username)
    return verified, username


def parseMessage(command):
    res = 'File after parsing:\n\t'
    word = ''
    for pos, char in enumerate(command):
        if re.match("[a-zA-Z]|-", char):
            word += char
        else:
            if word:
                res += f"[{word}]" if word.upper() in wordDict else word
                word = ''
            res += char
    return res


def handle_client(clientSocket):
    # Send the welcome message
    socket.send(socket.WELCOME, clientSocket)
    # Verify if the user is new
    socket.send(socket.USERNAME, clientSocket, DELAY_TIME)
    verified, username = verifyUsername(clientSocket)
    # send error msg if not a new user else ask to send the file
    if verified:
        insert("Client " + username + " added")
        socket.send(socket.USER_VERIFIED, clientSocket, DELAY_TIME)
        socket.send(socket.FILE, clientSocket, DELAY_TIME)
        # catch the file
        command = socket.receive(clientSocket)
        returnMsg = parseMessage(command)
        socket.send(returnMsg, clientSocket, DELAY_TIME)

    socket.send(socket.CONNECTION_CLOSE, clientSocket, DELAY_TIME)
    insert("Connection closed and " + username + " disconnected")
    userTable.remove(username)
    clientSocket.close()


def startServer():
# Get the client details after accepting a request and send the welcome message
    while True:
        clientSocket, (clientAdd, clientPort) = socket.socket.accept()
        connections.append(clientSocket)
        print(f"connection from {clientAdd, clientPort} has been established")
        insert(f"connection from {clientAdd, clientPort} has been established")
        thread = threading.Thread(target=handle_client, args=(clientSocket,))
        thread.start()
        pollingThread = threading.Thread(target=check_every_sixty_seconds, daemon=True)
        pollingThread.start()
#         activeCount = threading.activeCount() - 1
#         print(f"Number of Threads active:{activeCount}")



def createSocketAndStart():
    global socket
    try:
        socket = SocketClass("localhost", 9000, server=True)
    except (ConnectionRefusedError, ConnectionResetError) as e:
        insert(e.strerror)
        return
    insert("Localhost server listening at port 9000...")
#     startServer()
    rcv = threading.Thread(target=startServer)
    rcv.start()





# ###############  FRAME1[Server Info]  ############################
# Frame2 has {Server} title label, {Address} and {Port} input boxes and {Connect} button
# #####################################################
frame1 = tk.Frame(master=master, width=600, height=110, bg=backgroundColor)

tk.Label(
    frame1, text="Server", font=titleFont, bg=backgroundColor, fg="bisque", justify="center").place(x=250, y=1)
connButton = tk.Button(
    frame1, text="Start", command=createSocketAndStart, font=subTitleFont,
                       bg=backgroundColor, fg="bisque", pady=buttonPady, padx=buttonPadx)

# connButton = tk.Button(
#     frame1, text="Connect", command=connectionHandler, state=tk.NORMAL, font=subTitleFont,
#                        bg=backgroundColor, fg="bisque", pady=buttonPady, padx=buttonPadx)
connButton.place(x=250, y=68)

# frame1.wm_attributes("-transparentcolor", backgroundColor)
frame1.pack()

# ############# Scrollable #############################
# Scrollable Console Log
# #######################################################
textArea = st.ScrolledText(master=master, bg=backgroundColor, fg="bisque", padx=10, pady=5, font=("Courier", 10), height=15)
textArea.pack()

# ################## Exit button ###########################
tk.Button(master, text='Exit', command=master.quit, font=("Arial", 10), bg="grey", fg="bisque", pady=.8, padx=10).pack(
    side="bottom")




master.mainloop()
