import socket


def server(host='0.0.0.0', port=17300):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    conn, addr = s.accept()
    print 'connected by', addr
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print data
        conn.send(data)
    conn.close()


if __name__ == '__main__':
    server()
