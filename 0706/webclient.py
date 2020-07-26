import socket

HOST = input('ホスト名を入力 >> ')
PORT = input('ポート番号を入力 >> ')

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, int(PORT)))
    except:
        exit()

    req_line = 'GET / HTTP/1.1\r\n'
    req_head = 'HOST: %s\r\n' % (HOST)
    blank_line = '\r\n'

    sock.sendall(req_line.encode('utf-8'))
    sock.sendall(req_head.encode('utf-8'))
    sock.sendall(blank_line.encode('utf-8'))
