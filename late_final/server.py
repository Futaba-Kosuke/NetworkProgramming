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

    def run (self, mode: str = 'bbs') -> None:
        print('start server')
        while True:
            sock_c, addr = self.sock.accept()
            if mode == 'bbs':
                multiprocessing.Process(target=self.bulletin_board, args=(sock_c, addr)).start()
            elif mode == 'chat':
                self.chat(sock_c, addr)

    def bulletin_board (self, sock_c: socket.socket, addr: str) -> None:
        req_json = sock_c.recv(self.buf_size).decode('utf-8')
        req_dict = json.loads(req_dict)
        mode = req_dict['mode']

        # メッセージ投稿
        if mode == 'post':
            post_json = req_dict['json']
            message = Message(post_json)

            with open('log/log.json', 'r') as f:
                log_dict = json.load(f)

            log_dict['log'].append(message.to_dict(is_have_secret=True))

            with open('log/log.json', 'w') as f:
                json.dump(log_dict, f, indent=4)

            return 

        # ログ呼び出し
        if mode == 'read':
            with open('log/log.json', 'r') as f:
                log_dict = json.load(f)

            # クライアントに送るべきでないデータを除去
            log_dict['log'] = [Message(json.dumps(log)).to_dict(is_have_secret=False) for log in log_dict['log']]
            print(log_dict)
            sock_c.send(json.dumps(log_dict).encode('utf-8'))

            return

        if mode == 'delete':
            post_json = req_dict['json']
            post_dict = json.loads(post_json)
            target_id, password = post_dict['target_id'], post_dict['password']

            with open('log/log.json', 'r') as f:
                log_dict = json.load(f)
            log_dict['log'] = [Message(json.dumps(log)).to_dict(is_have_secret=True) for log in log_dict['log']]

            target_idx = [i for i, message in enumerate(log_dict['log'])
                                if message['unique_id'] == target_id and message['password'] == sha256_add(password, message['date'])
                             ]

            print(log_dict)
            log_dict['log'].pop(target_idx[0])

            with open('log/log.json', 'w') as f:
                json.dump(log_dict, f, indent=4)

            return

        sock_c.close()

    def chat (self, sock_c: socket.socket, addr: str) -> None:
        multiprocessing.Process(target=self.recv_process, args=(sock_c, addr)).start()
        self.send_process(sock_c, addr)

    def recv_process (self, sock_c: socket.socket, addr: str) -> None:
        while True:
            message_json = sock_c.recv(BUFSIZE).decode('utf-8')
            message = Message(message_json)
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

        return

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-addr', '--address', default=DEFAULT_STATUS['address'])
    parser.add_argument('-p', '--port', default=DEFAULT_STATUS['port'])

    args = parser.parse_args()
    address = args.address
    port = args.port

    server = Server(buf_size=BUFSIZE, address=address, port=port)
    server.run(mode='chat')

if __name__ == '__main__':
    main()
