# coding: utf-8
import socket, os, threading, sys, string
import controller, port

PORT = port.PORT
size = 1024
myPath = os.path.dirname(os.path.realpath(__file__)) + '/client/'

def socketInit(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip,PORT))
    return sock

def hostClient(ip):
    sock = socketInit(ip)
    print('Connected')

    try:
        clientRx = threading.Thread(target = controller.rxThread, args=(sock, myPath, "client"))
        clientTx = threading.Thread(target = controller.txThread, args=(sock, myPath))
        clientRx.start()
        clientTx.start()
    except:
        print("Unable to start Client Thread")

    while (clientTx.is_alive() == True or clientRx.is_alive() == True):
        clientRx.join()
        clientTx.join()

    sock.close()
