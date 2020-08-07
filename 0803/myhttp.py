import datetime

BUFSIZE = 1024
WAIT_TIME = 1

statusline = 'HTTP/1.1 200 OK\r\n'
blank_line = '\r\n'
contents = 'いいよ〜'

def recv_crlf(sock_c):
    BUFSIZE_CRLF = 1

    req = ''
    while req.find('\r\n') < 0:
        data = sock_c.recv(BUFSIZE_CRLF)
        if not data:
            break
        req += data.decode('utf-8')

    return req

def get_request(sock_c):

    sock_c.settimeout(WAIT_TIME)

    req_l = req_h = req_m = None

    try:
        req = recv_crlf(sock_c)
        i_CRLF = req.find('\r\n')
        if i_CRLF < 0:
            print('No Request Line')
            return (None, None, None)
        req_l = req[:i_CRLF]

        req_h = {}
        key_value = recv_crlf(sock_c)
        while key_value != '\r\n':
            k, v = key_value.split(': ')
            req_h[k] = v[:-2]
            key_value = recv_crlf(sock_c)

        if 'Content-Length' in req_h:
            req_m = sock_c.recv(BUFSIZE).decode('utf-8')
            while len(req_m) < int(req_h['Content-Length']):
                data = sock_c.recv(BUFSIZE)
                if not data:
                    break
                req_m += data.decode('utf-8')

    except:
        pass

    return (req_l, req_h, req_m)


def send_response(sock_c, code, phrase, f):
    statusline = '{} {} {}'.format('HTTP/1.1', code, phrase)
    
    dt_now = datetime.datetime.now()
    header = dt_now.strftime('Data: %a, %d %m %Y %H:%M:%S JST\r\n')

    if f != None:
        body = f.read()
        header += 'Content-Length: {}\r\n'.format(len(body))

        extension_index = f.name.rindex('.')
        extension = f.name[-extension_index + 1:].lower()

        if extension == 'html' or extension == 'htm':
            header += 'Content-Type: {}\r\n'.format('text/html')
        elif extension == 'txt':
            header += 'Content-Type: {}\r\n'.format('text/plain')
        elif extension == 'gif':
            header += 'Content-Type: {}\r\n'.format('image/gif')
        elif extension == 'png':
            header += 'Content-Type: {}\r\n'.format('image/png')

    else:
        body = None

    sock_c.sendall(statusline.encode('utf-8'))
    sock_c.sendall(header.encode('utf-8'))
    sock_c.sendall('\r\n'.encode('utf-8'))
    if body != None:
      sock_c.sendall(body)
