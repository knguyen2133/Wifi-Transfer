from bluetooth import *
import time, threading, socket, network_ip, Queue

def serverTxThread(client_sock, ipQueue):
    sendData =  network_ip.getIp()
    client_sock.send(sendData)
    ipQueue.put(sendData)
    time.sleep(1)

def serverRxThread(client_sock):
    data = client_sock.recv(1024)
    #print("Client IP: %s" % data)
    time.sleep(1)

def hostServerBt():
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
    ip = 0

    try:
        serverRx = threading.Thread(target = serverRxThread, args=(client_sock,))
        serverTx = threading.Thread(target = serverTxThread, args=(client_sock,ipQueue,))
        serverRx.start()
        serverTx.start()
    except:
        print("Unable to start Server Thread")

    while (serverTx.is_alive() == True):
        serverRx.join()
        serverTx.join()

    client_sock.close()
    server_sock.close()

    ip = ipQueue.get()

    return ip
