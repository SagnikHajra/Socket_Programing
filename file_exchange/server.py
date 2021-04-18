#!/usr/bin/python3
from SocketFunc import SocketClass
import threading
import re

# Create a socket and the listen for any client, once a connection is established with a client, communicate with it.
class server(SocketClass):
    def __init__(self):
        self.database = {}
        self.ADD = 'localhost'
        self.PRT = 9000
        self.command = ''
        self.userTable = set()
        self.DELAY_TIME = 0.1
        self.wordList = "ALICE DAISY-CHAIN DAISIES WHITERABBIT WAISTCOAT-POCKET DINAH DUCHESS GRYPHON BILL PETER BAYARD LORY PAT FOOTMAN".split(" ")
        self.wordDict = {x.strip() for x in self.wordList}

        super(server, self).__init__(self.ADD, self.PRT, server=True, clientLimit=3)

    # the below function interprets the file recv from client
    def parseMessage(self):
        res = 'File after parsing:\n\t'
        word = ''
        for pos, char in enumerate(self.command):
            if re.match("[a-zA-Z]|-", char):
                word += char
            else:
                if word:
                    res += f"[{word}]" if word.upper() in self.wordDict else word
                    word = ''
                res += char
        return res

    # If the user is already connected then ask for other username or else add the username and move further
    # Once the user is disconnected, remove from userTable. The handle_client func does it
    def verifyUsername(self, clientSocket, counter=0):
        if counter > 3:
            return False
        self.send(self.USERNAME, clientSocket, self.DELAY_TIME)
        username = self.receive(clientSocket)
        if username in self.userTable:
            self.send(self.USER_INVALID, clientSocket, self.DELAY_TIME)
            verified = self.verifyUsername(clientSocket, counter+1)
        else:
            verified = True
            self.userTable.add(username)
        return verified, username

    # Handle each client separated by threading
    def handle_client(self, clientSocket):
        # Send the welcome message
        self.send(self.WELCOME, clientSocket)
        # Verify if the user is new
        verified, username = self.verifyUsername(clientSocket)
        # send error msg if not a new user else ask to send the file
        if verified:
            self.send(self.USER_VERIFIED, clientSocket, self.DELAY_TIME)
            self.send(self.FILE, clientSocket, self.DELAY_TIME)
            # catch the file
            self.command = self.receive(clientSocket)
            returnMsg = self.parseMessage()
            self.send(returnMsg, clientSocket, self.DELAY_TIME)

        self.send(self.CONNECTION_CLOSE, clientSocket, self.DELAY_TIME)
        self.userTable.remove(username)
        clientSocket.close()

    # Connects with the client, recv command from client, parse the command and respond back
    def start(self):
        # Get the client details after accepting a request and send the welcome message
        while True:
            clientSocket, (clientAdd, clientPort) = self.socket.accept()
            print(f"connection from {clientAdd, clientPort} has been established")
            thread = threading.Thread(target=self.handle_client, args=(clientSocket, ))
            thread.start()
            activeCount = threading.activeCount() - 1
            print(f"Number of Threads active:{activeCount}")

if __name__ == "__main__":
    # let the game begin
    s = server()
    s.start()
