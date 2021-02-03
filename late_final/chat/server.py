import sys
import socket
import argparse
from dataclasses import dataclass, InitVar, field
import json
import threading
import multiprocessing

from utils.utils import sha256, sha256_add
from utils.message import Message

BUFSIZE = 8192
DEFAULT_STATUS = {
        'address': '',
        'port': 50000
    }

@dataclass
class Server:
    buf_size: int

    address: InitVar[str]
    port: InitVar[int]

    sock: socket.socket = field(default=socket.socket())
    
    def __post_init__ (self, address, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((address, port))
        self.sock.listen()

    def __del__ (self):
        self.sock.close()

    def run (self) -> None:
        print('start server')
        while True:
            sock_c, addr = self.sock.accept()
            self.chat(sock_c, addr)

    def chat (self, sock_c: socket.socket, addr: str) -> None:
        p = multiprocessing.Process(target=self.recv_process, args=(sock_c, addr))
        p.deamon = True
        p.start()
        self.send_process(sock_c, addr)

    def recv_process (self, sock_c: socket.socket, addr: str) -> None:
        while True:
            message_json = sock_c.recv(BUFSIZE).decode('utf-8')
            message = Message(message_json)
            if message.letter == 'bye':
                print(f'OK, bye {message.user_name}')
                break

            green_color = '\033[32m'
            end_color = '\033[0m'
            print(f'\n{green_color}{message.letter:>40}{end_color}')

        return 

    def send_process (self, sock_c: socket.socket, addr: str) -> None:
        while True:
            letter = input()

            date = 'XXX'
            unique_id = 'XXX'
            user_name = 'SERVER'
            title = 'XXX'
            letter = letter
            user_ip = 'XXX'
            password = 'XXX'
            
            message = Message(
                message_json=json.dumps({
                    'unique_id': unique_id,
                    'user_name': user_name,
                    'date': date,
                    'title': title,
                    'letter': letter,
                    'user_ip': user_ip,
                    'password': password
                })
            )
 
            sock_c.send(message.to_json(is_have_secret=False).encode('utf-8'))

            if letter == 'bye':
                print(f'OK, bye {message.user_name}')
                break

        return

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-addr', '--address', default=DEFAULT_STATUS['address'])
    parser.add_argument('-p', '--port', default=DEFAULT_STATUS['port'])

    args = parser.parse_args()
    address = args.address
    port = args.port

    server = Server(buf_size=BUFSIZE, address=address, port=port)
    server.run()

if __name__ == '__main__':
    main()
