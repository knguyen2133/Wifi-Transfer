import os, sys, string, time, socket

def listDirectory(myPath) :

    fileList = []
    for itemPath in os.listdir(myPath):
        itemPath = os.path.join(myPath, itemPath)
        if os.path.isfile(itemPath) and (itemPath.find("/.") == -1):
            item = itemPath.split(myPath)
            fileList.append(item[1])

    fileList.sort()
    fileList.append('ENDOFFILE')

    return fileList

def displayMyDir(path):
    count = 0
    fileList = listDirectory(path)
    while fileList[count] != 'ENDOFFILE':
        print("%d. %s" % (count+1, fileList[count]))
        count+=1

def printFileList(fileList):
    count = 0
    while fileList[count] != 'ENDOFFILE':
        print("%d. %s" % (count+1, fileList[count]))
        count+=1

def sendUpdateDir(sock, myPath):
    sock.send("PEERDIR")
    fileList = listDirectory(myPath)
    for item in fileList:
        time.sleep(1)
        res = sock.send(item)

def recvUpdateDir(sock):
    fileList = []
    item = sock.recv(1024)
    fileList.append(item)

    while item != 'ENDOFFILE':
        item = sock.recv(1024)
        fileList.append(item)
    return fileList

def findMyFilename(myPath, num):
    fileList = listDirectory(myPath)
    return fileList[num]

def sendFile(sock, myPath, peer, num):
    filename = findMyFilename(myPath, num)
    sock.send("SENDING")
    time.sleep(1)
    sock.send(filename)
    f = open(peer + '/' + filename, 'r')
    for line in f:
        time.sleep(1)
        sock.send(line)

    time.sleep(1)
    sock.send("ENDOFFILE")

def recvFile(sock, peer):
    filename = sock.recv(1024)
    f = open(peer + '/' + filename, 'wb')
    item = sock.recv(1024)
    while item != "ENDOFFILE":
        f.write(item)
        item = sock.recv(1024)

    f.close()
    print "WRITE SUCCESSFUL"
