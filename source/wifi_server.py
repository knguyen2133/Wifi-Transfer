# coding: utf-8
import socket, os, threading, sys, string
import controller, port

port = port.PORT
size = 1024
backlog = 5
myPath = os.path.dirname(os.path.realpath(__file__)) + '/server/'

def socketInit(ip):
    serverID = socket.gethostbyname(socket.gethostname())
    info = 'SERVER ID: {} port: {}'.format(serverID, port)
    print info

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip,port))
    sock.listen(backlog)
    #sock.setblocking(0)

    return sock

def hostServer(ip):
    sock = socketInit(ip)
    client, address = sock.accept()
    #client.setblocking(0)
    print('Connected')

    try:
        serverRx = threading.Thread(target = controller.rxThread, args=(client, myPath, "server"))
        serverTx = threading.Thread(target = controller.txThread, args=(client, myPath))
        serverRx.start()
        serverTx.start()
    except:
        print("Unable to start Server Thread")

    while (serverTx.is_alive() == True or serverRx.is_alive() == True):
        serverRx.join()
        serverTx.join()

    client.close()
    sock.close()
