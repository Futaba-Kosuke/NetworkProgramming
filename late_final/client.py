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
import getpass

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

    def run (self, mode: str = 'bbs') -> None:
        if mode == 'bbs':
            self.bulletin_board()
        elif mode == 'chat':
            self.chat()

        return 

    def bulletin_board (self) -> None:
        self.connect()

        mode = input('mode >> ')
        if mode == 'read':
            log_list = self.read()
            
            for message in log_list:
                print('===============================')
                print(f'ユーザー名: {message.user_name}')
                print(f'ID: {message.unique_id}')
                print(f'投稿時刻: {message.date}')
                print('-------------------------------')
                print(f'[{message.title}]')
                print(message.letter, '\n')

            return

        if mode == 'post':
            # 時刻のハッシュ値とランダム文字列を結合し、固有IDを生成
            date = datetime.datetime.now().strftime('%Y/%m/%d_%H:%M:%S')
            unique_id = sha256(date)[0:5] + '%x' % random.randrange(16**10)
            user_name = input('ユーザー名 >> ')
            title = input('タイトル >> ')
            letter = input('本文 >> ')
            user_ip = socket.gethostbyname(self.host)

            password_plain = getpass.getpass('パスワード >> ')
            password_secret = sha256(plain_text=password_plain)
            password_secure = sha256_add(secret_text=password_secret, addition=date)
            
            message = Message(
                message_json=json.dumps({
                    'unique_id': unique_id,
                    'user_name': user_name,
                    'date': date,
                    'title': title,
                    'letter': letter,
                    'user_ip': user_ip,
                    'password': password_secure
                })
            )
            self.post(message)

            return

        if mode == 'delete':
            target_id = input('ID >> ')
            password = hashlib.sha256(input('パスワード >> ').encode('utf-8')).hexdigest()
            self.delete(target_id=target_id, password=password)

            return

    def chat (self) -> None:
        self.connect()
        recv_p = multiprocessing.Process(target=self.recv_process)
        recv_p.start()
        self.send_process(recv_p)

    def send_process (self, recv_p: multiprocessing.Process) -> None:
        while True:
            letter = input()

            if letter == 'bye':
                print(f'OK, bye {user_name}')
                recv_p.kill()
                break

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

        return 

    def recv_process (self) -> None:
        while True:
            message_json = self.sock.recv(BUFSIZE).decode('utf-8')
            message = Message(message_json)
            green_color = '\033[32m'
            end_color = '\033[0m'
            print(f'\n{green_color}{message.letter:>40}{end_color}')

        return 

    def connect (self) -> None:
        self.sock.connect((self.host, self.port))
        is_connected = True

    def read (self) -> List[Message]:
        req = {
                'mode': 'read',
                'json': ''
              }
        self.sock.send(json.dumps(req).encode('utf-8'))
        log_json = self.sock.recv(BUFSIZE).decode('utf-8')
        log_list = json.loads(log_json)['log']
        return [Message(json.dumps(l)) for l in log_list]

    def post (self, message: Message) -> None:
        req = {
                'mode': 'post',
                'json': message.to_json(is_have_secret=True).encode('utf-8')
              }
        self.sock.send(json.dumps(req).encode('utf-8'))

    def delete (self, target_id: str, password: str) -> None:
        req = {
                'mode': 'delete',
                'json': {'target_id': target_id, 'password': password}
              }

        self.sock.send(json.dumps(req).encode('utf-8'))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-ho', '--host', default=DEFAULT_STATUS['host'])
    parser.add_argument('-p', '--port', default=DEFAULT_STATUS['port'])

    args = parser.parse_args()
    host = args.host
    port = args.port

    client = Client(buf_size=BUFSIZE, host=host, port=port)
    client.run(mode='chat')

if __name__ == '__main__':
    main()
