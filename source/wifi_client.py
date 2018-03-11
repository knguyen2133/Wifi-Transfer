import socket

def hostClient(s, ip):
    s.connect((ip, 8080))

    while True:
        data2 = raw_input()
        s.sendall(data2)
