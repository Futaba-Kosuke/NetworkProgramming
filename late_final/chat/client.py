import sys
import socket
import time
import argparse
from typing import List
from dataclasses import dataclass, InitVar, field
import json
import threading
import datetime
import hashlib
import random
import multiprocessing

from utils.utils import sha256, sha256_add
from utils.message import Message

BUFSIZE = 8192
DEFAULT_STATUS = {
        'host': '127.0.0.1',
        'port': 50000
    }

@dataclass
class Client:
    buf_size: int
    host: str
    port: int

    sock: socket.socket = field(default=socket.socket())
    is_connected: bool = field(default=False)

    def __post_init__ (self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__ (self):
        self.sock.close()

    def run (self) -> None:
        self.chat()

        return 

    def chat (self) -> None:
        self.connect()
        p = multiprocessing.Process(target=self.recv_process)
        p.deamon = True
        p.start()
        self.send_process()

    def send_process (self) -> None:
        while True:
            letter = input()

            date = 'XXX'
            unique_id = 'XXX'
            user_name = 'CLIENT'
            title = 'XXX'
            letter = letter
            user_ip = socket.gethostbyname(self.host)
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
            self.post(message)

            if letter == 'bye':
                print(f'OK, bye {user_name}')
                break

        return 

    def recv_process (self) -> None:
        while True:
            message_json = self.sock.recv(BUFSIZE).decode('utf-8')
            message = Message(message_json)
            if message.letter == 'bye':
                print(f'OK, bye {message.user_name}')
                break
            green_color = '\033[32m'
            end_color = '\033[0m'
            print(f'\n{green_color}{message.letter:>40}{end_color}')

        return 

    def connect (self) -> None:
        self.sock.connect((self.host, self.port))
        is_connected = True

    def post (self, message: Message) -> None:
        self.sock.send(message.to_json(is_have_secret=True).encode('utf-8'))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-ho', '--host', default=DEFAULT_STATUS['host'])
    parser.add_argument('-p', '--port', default=DEFAULT_STATUS['port'])

    args = parser.parse_args()
    host = args.host
    port = args.port

    client = Client(buf_size=BUFSIZE, host=host, port=port)
    client.run()

if __name__ == '__main__':
    main()
