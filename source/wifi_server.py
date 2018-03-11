import socket

def hostServer(s, ip):
    s.bind(('192.168.1.88', 8080))
    s.listen(1)
    conn, addr = s.accept()
    print 'Wifi Connected'
    #while 1:
    data = conn.recv(1024)
    print data
    if data == "Ping":
        print "Pong!"

    conn.close()
