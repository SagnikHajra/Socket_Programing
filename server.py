import socket


# Create a socket and the listen for any client, once a connection is established with a client, communicate with it.
class server:
    def __init__(self):
        self.database = {}
        self.HEADERSIZE = 10
        self.ADDRESS = 'localhost'
        self.PORT = 8912
        self.command = ''
        self.clientSocket = None

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.ADDRESS, self.PORT))
        self.serverSocket.listen(1)
        print(f"server {self.ADDRESS} started on port number {self.PORT}")

    # the below function interprets the command/request recv from client
    def parseMessage(self):
        msgList = self.command.strip().split(' ')
        if msgList[0].upper() == 'PUT':
            text = ' '.join(x for x in msgList[2:])
            return self.putMsg(msgList[1], text)
        elif msgList[0].upper() == 'GET':
            return self.getMsg(msgList[1])
        elif msgList[0].upper() == 'DUMP':
            return self.dumpMsg()
        else:
            return "Client request didn't have 'PUT' or 'GET' or 'DUMP' key word"

    # When PUT request received just add the key-value to the database
    def putMsg(self, key, text):
        self.database[key] = text
        # self.timetable[key] = time()
        return "msg received"

    # When GET request received just return the value of the key
    def getMsg(self, key):
        if key in self.database:
            # self.timetable[key] = time()
            return self.database[key]
        else:
            return 'None'

    # When dump request received, return all the keys of database
    def dumpMsg(self):
        return ' '.join(str(x) for x in self.database.keys())

    # Connects with the client, recv command from client, parse the command and respond/send back
    def start(self):
        while True:
            self.clientSocket, (clientAdd, clientPort) = self.serverSocket.accept()
            print(f"connection from {clientAdd, clientPort} has been established")
            msg = "Welcome to the server! What can I do for you?\n"
            msg = f"{len(msg):<{self.HEADERSIZE}}" + msg
            self.clientSocket.send(bytes(msg, "utf-8"))
            self.command = ''
            while self.clientSocket:
                msg = self.clientSocket.recv(1024)
                self.command += msg.decode('utf-8')
                if self.command[-1:] == '\n' or self.command[-1:] == '\r':
                    print(f"full msg is: {self.command}")
                    returnMsg = self.parseMessage()
                    self.clientSocket.send(bytes(str(returnMsg) + '\n', 'utf-8'))
                    self.command = ''


if __name__ == "__main__":
    # let the game begin
    s = server()
    s.start()
