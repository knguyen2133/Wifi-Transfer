# file: rfcomm-client.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a client application that uses RFCOMM sockets
#       intended for use with rfcomm-server
#
# $Id: rfcomm-client.py 424 2006-08-24 03:35:54Z albert $

from bluetooth import *
import sys, time, threading, socket, wifi, Queue

def clientTxThread(sock):
    try:
        sendData = wifi.get_lan_ip()
        sock.send(sendData)

        time.sleep(1)
    except IOError:
        print("Tx Failed")
        pass

def clientRxThread(sock, ipQueue):
    try:
        data = sock.recv(1024)
        if len(data) == 0: pass
        print("Server IP: %s" % data)

        time.sleep(1)
    except IOError:
        print("Rx Failed")
        pass

    ipQueue.put(data)

def clientBt(addr):
    print("You are Client")

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_matches = find_service( uuid = uuid, address = addr )

    if len(service_matches) == 0:
        print("Couldn't find the service")
        return

    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]

    print("Connecting to \"%s\" on %s" % (name, host))

    # Create the client socket
    sock=BluetoothSocket( RFCOMM )
    sock.connect((host, port))

    print("Connected")
    ipQueue = queue.Queue()

    try:
        clientRx = threading.Thread(target = clientRxThread, args=(sock,ipQueue,))
        clientTx = threading.Thread(target = clientTxThread, args=(sock,))
        clientRx.start()
        clientTx.start()

    except:
        print("Unable to start Client Thread")

    while (clientTx.is_alive() == True or clientRx.is_alive() == True):
        clientRx.join()
        clientTx.join()

    print("Disconnected\n\n")

    sock.close()

    ip = ipQueue.get()
    print ip

    return ip
