import socket
from myhttp import recv_crlf, get_request, send_response

MY_ADDRESS = ''
MY_PORT = 50000
BASE_DIR = '.'

if __name__ == '__main__':

    print('URL: http://localhost:%s/index.html\n' % (str(MY_PORT)))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((MY_ADDRESS, MY_PORT))
    sock.listen()

    while True:
        sock_c, addr = sock.accept()

        # try:
        line, header, body = get_request(sock_c)

        print('request line: %s\n' % (line))
        print('request header: %s\n' % (header))
        print('message body: %s\n' % (body))

        reql = line.split(' ')

        if reql[0] == 'GET':
            filepath = BASE_DIR + reql[1]
            try:
                with open(filepath, 'rb') as f:
                    # pass
                    send_response(sock_c, 200, 'OK', f)
            except:
                with open(BASE_DIR + '/404.html', 'rb') as f:
                    send_response(sock_c, 404, 'Page Not Found', f)
        else:
            send_response(sock_c, 501, 'Not Implemented', None)
        # except:
        #     send_response(sock_c, 500, 'Internal Server Error', None)


        sock_c.close()

    sock.close()
