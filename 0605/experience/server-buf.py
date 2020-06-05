import socket

# 1. ソケットの作成
"""
第4層: TCP
第3層: IPv4
"""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. ソケットへ自分の情報を登録
sock.bind(("", 50000))

while True:
    # 3. 誰かの接続を待つ
    sock.listen()

    # 4. 接続要求に応える
    sock_c, addr = sock.accept()

    msg = '4433'

    try:
        sock_c.sendall(msg.encode('utf-8'))
        sock_c.sendall(msg.encode('utf-8'))
    except:
        print('sendall function failed.')

    # 5. ソケットを閉じる
    sock_c.close()

sock.close()
