import socket
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# localhost上で動いているサーバーを指定
HOST = '127.0.0.1'
PORT = 50000

sock.connect((HOST, PORT))

BUFSIZE = 256
data = sock.recv(BUFSIZE)

print(data.decode('UTF-8'))

sock.close()
