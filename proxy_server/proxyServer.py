from server import server
import socket
from time import time


# Create two sockets, one socket binds the address and port number as a server and
# another TCP/IP socket works as a client to the main server.
class proxyServer:
    def __init__(self):
        self.cache = {}
        self.timetable = {}
        self.HEADERSIZE = 10
        self.ADDRESS = 'localhost'
        self.command = ''
        self.clientSocket = None
        self.last_time = time()
        self.OWN_PORT = 7891
        self.SERVER_PORT = 8912

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind((self.ADDRESS, self.OWN_PORT))
        self.serverSocket.listen(1)
        print(f"server {self.ADDRESS} started on port number {self.OWN_PORT}")

        self.tcpServerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Avoid error 'Address already in use'.
        self.tcpServerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpServerSock.connect((self.ADDRESS, self.SERVER_PORT))
        self.tcpMsg = ''
        # below part is to ack the connection is established.
        while self.tcpMsg == '':
            self.tcpMsg = self.tcpServerSock.recv(1024).decode('utf-8')
        print(self.tcpMsg)

    # Here, tcpServerSock is behaving as a client to the main server and sending/recving msges
    # One can assume that once connected, the tcpServer socket will remain open until server and/or proxy is down
    def proxyToMainServer(self):
        print("Connecting server..")
        new_msg = False
        full_msg = ''
        self.tcpServerSock.send(bytes(self.command, 'utf-8'))
        while new_msg is False:
            full_msg += self.tcpServerSock.recv(1024).decode('utf-8')
            if full_msg:
                new_msg = True
        return full_msg


    # delete from cache if NO client has asked(GET) for the key in the last 60 sec
    def updateCache(self):
        deleted = []
        for key, value in self.timetable.items():
            if time() - value > 60.0:
                deleted.append(key)
        for keys in deleted:
            del self.timetable[keys]
            del self.cache[keys]

    # the below function interprets the command/request recv from client
    def parseCommand(self):
        msgList = self.command.strip().split(' ')
        if msgList[0].upper() in ('PUT', 'DUMP'):
            return self.putOrDumpMsg()
        elif msgList[0].upper() == 'GET':
            return self.getMsg(msgList[1])
        else:
            return "Client request didn't have 'PUT' or 'GET' or 'DUMP' key word"

    # When PUT/DUMP request received, just pass that to the server.
    def putOrDumpMsg(self):
        return self.proxyToMainServer()

    # When GET request received from Client.
    #   Proxy server checks the cache and if found returns the val else
    #       reaches out to Server.
    #       The server returns the string "Sagnik Hajra" to the proxy server
    #       The proxy server cache the key-val {name : Sagnik Hajra} as well as update the timestamp in the timetable
    def getMsg(self, key):
        if key in self.cache:
            self.timetable[key] = time()
            return str(self.cache[key])
        else:
            res = self.proxyToMainServer()
            if res != 'None':
                self.cache[key] = res
                self.timetable[key] = time()
            else:
                res = f"{key} not found"
            return res

    # This is where most of the magics are happening.
    # Connects with the client, recv command from client, parse the command, send back msg to client and
    # at last, update the cache every 1 minute.
    def start(self):
        while True:
            # accept msg from client
            self.clientSocket, (clientAdd, clientPort) = self.serverSocket.accept()
            print(f"connection from {clientAdd, clientPort} has been established")
            msg = "Welcome to the Proxy server! But why??\n"
            # Headersize implementation wasn't needed, it was just for fun(being familiar with the concept)
            msg = f"{len(msg):<{self.HEADERSIZE}}" + msg
            self.clientSocket.send(bytes(msg, "utf-8"))
            self.command = ''
            while True:
                msg = self.clientSocket.recv(1024)
                self.command += msg.decode('utf-8')
                if self.command[-1:] == '\n' or self.command[-1:] == '\r':
                    print(f"full msg is: {self.command}")
                    returnMsg = self.parseCommand()
                    self.clientSocket.send(bytes(str(returnMsg) + '\n', 'utf-8'))
                    self.command = ''
                # update cache and remove keys older than 60 sec
                if time() - self.last_time > 60.0:
                    self.updateCache()
                    self.last_time = time()


if __name__ == "__main__":
    # let the game begin
    ps = proxyServer()
    ps.start()