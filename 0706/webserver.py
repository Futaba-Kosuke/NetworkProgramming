import socket

HOST = ''
PORT = 50000
BUFSIZE = 1024

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()

    while True:
        sock_c, addr = sock.accept()

        req = sock_c.recv(BUFSIZE)
        print(req.decode('utf-8'))

        try:
            sock_c.sendall('いいよ〜'.encode('utf-8'))
        except:
            print('failed to sendall')

        sock_c.close()

    sock.close()
