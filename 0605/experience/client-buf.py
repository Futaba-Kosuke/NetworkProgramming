import socket
import signal
import time

signal.signal(signal.SIGINT, signal.SIG_DFL)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# localhost上で動いているサーバーを指定
HOST = '127.0.0.1'
PORT = 50000
BUFSIZE = 8

sock.connect((HOST, PORT))

print('[sleep a little...]')
time.sleep(3)
print('[wake up!]')

data = sock.recv(BUFSIZE)
print('[received]')
print(data.decode('UTF-8'))

print('[sleep a little...]')
time.sleep(3)
print('[wake up!]')

data = sock.recv(BUFSIZE)
print('[received]')
print(data.decode('UTF-8'))

sock.close()
