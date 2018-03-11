import socket

def hostServer(s, ip):
    s.bind((ip, 8080))
    s.listen(1)
    conn, addr = s.accept()

    print ('I am Server')
    print 'Wifi Connected'
    #while 1:
    data = conn.recv(1024)
    print data
    if data == "Ping":
        print "Pong!"

    conn.close()
