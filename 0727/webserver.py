import socket

MY_ADDRESS = ''
MY_PORT = 50000
BUFSIZE = 1024
WAIT_TIME = 1

def recv_crlf(sock_c):
    BUFSIZE_CRLF = 1

    req = ''
    while req.find('\r\n') < 0:
        data = sock_c.recv(BUFSIZE_CRLF)
        if not data:
            break
        req += data.decode('utf-8')

    if req.find('\r\n') < 0:
        return None

    return req[:-2]

def get_request(sock_c):

    sock_c.settimeout(WAIT_TIME)

    try:
    
        req_l = recv_crlf(sock_c)
    
        req_h = {}
        pair = recv_crlf(sock_c)
        while pair != None and pair != '':
            key, value = pair.split(': ')
            req_h[key] = value
            pair = recv_crlf(sock_c)

        req_m = ''

        if 'Content-Length' in req_h:
            req_m = sock_c.recv(BUFSIZE).decode('utf-8')
            while len(req_m) < int(req_h['Content_Length']):
                data = sock_c.recv(BUFSIZE)
                if not data:
                    break
                req_m += data.decode('utf-8')

        return (req_l, req_h, None)

    except:
        return (None, None, None)

if __name__ == '__main__':

    print('URL: http://localhost:%s\n' % (str(MY_PORT)))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((MY_ADDRESS, MY_PORT))
    sock.listen()

    while True:
        sock_c, addr = sock.accept()

        line, header, body = get_request(sock_c)

        print('request line: %s\n' % (line))
        print('request header: %s\n' % (header))
        print('message body: %s\n' % (body))

        sock_c.close()

    sock.close()
