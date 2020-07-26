import socket

MY_ADDRESS = ''
MY_PORT = 50000
BUFSIZE = 1024

statusline = 'HTTP/1.1 200 OK\r\n'
blank_line = '\r\n'
contents = '''
<!DOCTYPE html>
<HTML>
<HEAD><META CHARSET=‘UTF-8’></HEAD>
<BODY>
<P>いいよ～</P>
</BODY>
</HTML>
'''


if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((MY_ADDRESS, MY_PORT))
    sock.listen()

    while True:
        sock_c, addr = sock.accept()

        req = sock_c.recv(BUFSIZE)
        print(req.decode('utf-8'))

        try:
            sock_c.sendall(statusline.encode('utf-8'))
            sock_c.sendall(blank_line.encode('utf-8'))
            sock_c.sendall(contents.encode('utf-8'))
        except:
            print('failed to sendall')

        sock_c.close()

    sock.close()
