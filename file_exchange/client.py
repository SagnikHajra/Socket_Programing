import os.path

from SocketFunc import SocketClass

closeSocket = False
socket = SocketClass('localhost', 9000)


def openFile(path):
    if os.path.isfile(path):
        return open(path, 'r').read()
    else:
        return ""


while not closeSocket:
    while True:
        serverMsg = socket.receive(socket.socket)
        if serverMsg == socket.CONNECTION_CLOSE:
            closeSocket = True
            break
        elif serverMsg == socket.USERNAME:
            clientData = input(socket.messages[serverMsg])
            clientData = clientData.strip()
            socket.send(clientData, socket.socket)
        elif serverMsg == socket.FILE:
            clientData = input(socket.messages[serverMsg])
            clientData = openFile(clientData)
            socket.send(clientData, socket.socket)
        elif serverMsg not in socket.messages:
            print(serverMsg)
            xy = open('Alice_converted.txt','w+')
            xy.write(serverMsg)
            xy.close()
        else:
            print(socket.messages[serverMsg])

print("Closing the client socket")
socket.socket.close()
