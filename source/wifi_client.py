import socket

def hostClient(s, ip):
    s.connect(('192.168.1.88', 8080))
    print ('Wifi Connected')
    while True:
        data2 = raw_input()
        s.sendall(data2)
