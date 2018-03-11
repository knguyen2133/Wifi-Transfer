# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *
import time, threading, socket, wifi, Queue

def serverTxThread(client_sock):
    try:
        sendData =  wifi.get_lan_ip()
        client_sock.send(sendData)

        time.sleep(1)
    except IOError:
        print("Tx Failed")
        pass

def serverRxThread(client_sock, ipQueue):
    try:
        data = client_sock.recv(1024)
        if len(data) == 0: pass
        print("Client IP: %s" % data)

        time.sleep(1)
    except IOError:
        print("Rx Failed")
        pass

    ipQueue.put(data)

def serverBt():
    print("You are Server")

    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(.01)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service( server_sock, "Server",
                       service_id = uuid,
                       service_classes = [ uuid, SERIAL_PORT_CLASS ],
                       profiles = [ SERIAL_PORT_PROFILE ],
    #                   protocols = [ OBEX_UUID ]
                        )

    print("Waiting for connection on RFCOMM channel %d" % port)

    server_sock.settimeout(7);
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)
    ipQueue = Queue.Queue()

    try:
        serverRx = threading.Thread(target = serverRxThread, args=(client_sock,ipQueue,))
        serverTx = threading.Thread(target = serverTxThread, args=(client_sock,))
        serverRx.start()
        serverTx.start()
    except:
        print("Unable to start Server Thread")

    while (serverTx.is_alive() == True or serverRx.is_alive() == True):
        serverRx.join()
        serverTx.join()

    print("Disconnected\n\n")

    client_sock.close()
    server_sock.close()

    ip = ipQueue.get()
    print ip

    return ip
