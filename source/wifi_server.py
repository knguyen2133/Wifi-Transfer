import socket

def hostServer(s, ip):
    s.bind((ip, 8080))
    s.listen(1)
    conn, addr = s.accept()
    print 'Connected by', addr
    #while 1:
    data = conn.recv(1024)
    print data
    if data == "Ping":
        print "Pong!"

    conn.close()
