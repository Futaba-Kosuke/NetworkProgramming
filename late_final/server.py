import socket
import argparse
from dataclasses import dataclass, InitVar
import json
import threading

BUFSIZE = 1024

@dataclass
class Server:
    buf_size: int

    address: InitVar[str]
    port: InitVar[int]

    sock: socket.socket
    
    def __post_init__ (self, address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((address, port))
        self.sock.listen()

    def run (self) -> None:
        while True:
            sock_c, addr = self.sock.accept()
            threading.Thread(target=self.bulletin_board, args=(sock_c, addr)).start()

    def bulletin_board (self, sock_c: socket.socket, addr: str) -> None:
        post_json = sock_c.recv(self.buf_size).decode('utf-8')
        post_dict = json.loads(post_json)

        with open('log.json', 'r') as f:
            log_dict = json.load(f)

        log_dict['log'].append(post_dict)

        sock_c.send(json.dumps(log_dict).encode('utf-8'))
        
        with open('log.json', 'w') as f:
            json.dump(log_dict, f, indent=4)

        sock_c.close()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-addr', '--address', default='')
    parser.add_argument('-p', '--port', default=50000)

    args = parser.parse_args()
    address = args.address
    port = args.port

    server = Server(buf_size=BUFSIZE, address=address, port=port)
    server.run()

if __name__ == '__main__':
    main()
