import time, socket, os, sys
import dir_commands

def txThread(sock, path):

    try:
        txDone = False
        while not txDone:
            print("\nMENU:\n1.See My Directory\n2.See Peer Directory\n3.Request a File")
            print("4.Quit\n")
            userInput = raw_input(">> ")
            txDone = txController(sock, path, userInput)

            time.sleep(1)

    except (IOError, KeyboardInterrupt) as e:
        print("Tx Thread Closed")
        pass



def rxThread(sock, path, peer):
    try:
        rxDone = False
        while not rxDone:
            option = sock.recv(1024)
            rxDone = rxController(sock, path, option, peer)

            time.sleep(1)

    except (IOError, KeyboardInterrupt) as e:
        print("Rx Thread Closed")
        pass

def txController(sock, path, input):

    if (input == '1'):
        dir_commands.displayMyDir(path)

    elif(input == '2'):
        sock.send("UPDATE")
        time.sleep(5)

    elif(input == '3'):
        #display Peer Directory
        sock.send("UPDATE")
        time.sleep(5)

        sock.send("REQUEST")

        print("\nWhich number?")
        num = int(raw_input(">> ")) -1
        sock.send(str(num))
        time.sleep(5)

    elif(input == '4'):
        sock.send("SHUTDOWN")
        return True

    return False

def rxController(sock, path, option, peer):
    if (option == "UPDATE"):
        dir_commands.sendUpdateDir(sock, path)

    elif (option == "REQUEST"):
        num = sock.recv(1024)
        dir_commands.sendFile(sock, path, peer, int(num))

    elif(option == "PEERDIR"):
        fileList = dir_commands.recvUpdateDir(sock)
        dir_commands.printFileList(fileList)

    elif(option == "SENDING"):
        dir_commands.recvFile(sock, peer)

    elif(option == "SHUTDOWN"):
        return True

    return False
