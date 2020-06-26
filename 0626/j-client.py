# Mac/iTerm2で不必要
# import signal
# signal.signal(signal.SIGINT, signal.SIG_DFL)

import socket

HOST = '127.0.0.1'
PORT = 50000
BUFSIZE = 2048

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

rule = sock.recv(BUFSIZE)
print(rule.decode('utf-8'))

while True:
    hand = input('出す手は … ')

    sock.sendall(hand.encode('utf-8'))
    result = sock.recv(BUFSIZE)

    print(result.decode('utf-8'))

    if hand == '3':
        break

sock.close()
