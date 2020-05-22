import socket

while True:
    hostname = input('input hostname >> ')
    if hostname is 'q':
        break
    try:
        host = socket.gethostbyname(hostname)
        print(host)
        print('(10)\t->\t(2)')
        for octet in host.split('.'):
            print('%03d\t->\t%08d' % (int(octet), int(bin(int(octet))[2:])))
    except:
        print('(´・ω・｀)')
