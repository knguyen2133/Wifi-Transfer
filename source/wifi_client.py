import socket

def hostClient(s, ip):
    s.connect((ip, 8080))
    print ('I am Client')
    print ('Wifi Connected')
    while True:
        data2 = raw_input()
        s.sendall(data2)
