from bluetooth import *
import sys, time, threading, socket, network_ip, Queue
import port

def clientTxThread(sock):
    sendData = network_ip.getIp()
    sock.send(sendData)
    time.sleep(1)

def clientRxThread(sock, ipQueue):
    data = sock.recv(1024)
    print("Server IP: %s" % data)
    ipQueue.put(data)
    time.sleep(1)


def hostClientBt(addr):
    print("You are Client")

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_matches = find_service( uuid = uuid, address = addr )

    if len(service_matches) == 0:
        print("Couldn't find the service")
        return 0

    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]

    print("Connecting to \"%s\" on %s" % (name, host))

    # Create the client socket
    sock=BluetoothSocket( RFCOMM )
    sock.connect((host, port))

    print("Connected")
    ipQueue = Queue.Queue()
    ip = 0

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

    sock.close()

    ip = ipQueue.get()

    return ip
