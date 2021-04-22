import socket
import time


class SocketClass:
    def __init__(self, add, port, server=False, clientLimit=1):
        self.ADDRESS = add
        self.PORT = port
        self.HEADER_SIZE = 10
        self.MSG_SIZE = 1024
        self.FORMAT = 'utf-8'

        self.WELCOME = "Welcome"
        self.USERNAME = "Username"
        self.FILE = "File"
        self.USER_INVALID = "USER_INVALID"
        self.USER_VERIFIED = "USER_VERIFIED"
        self.CONNECTION_CLOSE = "CONNECTION_CLOSE"
        self.POOL = "POLLING"

        self.messages = {
            self.WELCOME: "Welcome to server",
            self.USERNAME: 'Username:',
            self.FILE: 'Upload the file:',
            self.USER_INVALID: "Error:- Connection rejected, user already connected",
            self.USER_VERIFIED: "Success:- Username added",
            self.CONNECTION_CLOSE: "Gotcha. Closing the connection...",
            self.POOL: "Got polling message"
        }
        if server:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.ADDRESS, self.PORT))
            self.socket.listen(clientLimit)
            print(f"server {self.ADDRESS} started on port number {self.PORT}")
            # self.clientSocket = None
            self.clientAdd = None
            self.clientPort = None
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ADDRESS, self.PORT))

    def receive(self, sock):
        command = ''
        new_msg = True
        msgLen = 0
        while True:
            msg = sock.recv(self.MSG_SIZE)
            if new_msg and msg:
                msgLen = int(msg[:self.HEADER_SIZE])
                new_msg = False
            command += msg.decode(self.FORMAT)
            if len(command) - self.HEADER_SIZE == msgLen:
                return command[self.HEADER_SIZE:]

    def send(self, returnMsg, sock, sleep=0):
        returnMsg = f"{len(returnMsg):<{self.HEADER_SIZE}}" + returnMsg
        time.sleep(sleep)
        sock.send(bytes(returnMsg, self.FORMAT))
