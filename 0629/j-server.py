# Mac/iTerm2で不必要
# import signal
# signal.signal(signal.SIGINT, signal.SIG_DFL)

import socket
import random
import threading

def janken(sock_c, addr):

    hand = ('やせ我慢', '愛情', '小切手')

    result = {
        'win': 0,
        'lose': 0,
        'draw': 0
    }

    count = 1

    try:
        print('%sから接続がありましたので、ゲームを開始します' % (addr,))
        sock_c.sendall(MESSAGE.encode('utf-8'))
    except:
        print('failed...')

    while True:
        
        count += 1

        try:
            data = sock_c.recv(BUFSIZE)
            data_pattern = (b'0', b'1', b'2', b'3')
            if not (data in data_pattern):
                msg = 'ルール通りに0～3を送ってくれなきゃ怒っちゃうぞっ！もういっかい入力してね！'
                sock_c.sendall(msg.encode('utf-8'))
                continue

            hand_client = int(data)
            
            if hand_client == 3:
                msg = 'あら？終わるのね。あなたの戦績は%d勝%d敗%d分だったよ！じゃ～ね～！' % (result['win'], result['lose'], result['draw'])
                sock_c.sendall(msg.encode('utf-8'))
                break

            hand_server = random.randint(0, 2)
            msg = 'あなた：%s<--->わたし：%s\n' % (hand[hand_client], hand[hand_server])
            
            '''
            0: 引き分け
            1: 勝ち
            2: 負け
            '''
            if (hand_client - hand_server + 3) % 3 == 0:
                msg += '引き分け！相性抜群かもね！\n'
                result['draw'] += 1
            elif (hand_client - hand_server + 3) % 3 == 1:
                msg += 'やった～わたしの勝ち！\n'
                result['lose'] += 1
            else:
                msg += 'あなたの勝ちかぁ！強いね！\n'
                result['win'] += 1

            msg += '---\n【%d回戦】\tどの手にする？' % (count, )
            
            sock_c.sendall(msg.encode('utf-8'))

        except:
            print('送受信エラーが発生したので%sとの通信を終了します' % (addr,))
            break

HOST = ''
PORT = 50000
BUFSIZE = 256
MESSAGE = '''------------------------------------------
■■■■■■■■■■
北九州工業高等専門学校　生産デザイン工学科　情報システムコース
4年通年科目「ネットワークプログラミング」課題用プログラム　ver.2020-1。
■■■■■■■■■■

■　ゲームの概要
　このゲームは0～2のうち一つの数字を互いに出して勝敗を決めるゲームだよ。
■　数字の対応
　0->やせ我慢　　1->愛情　　2->小切手　　3->ゲーム終了
■　強い/弱いの規則
「やせ我慢」をしているヤンキーも「愛情」を見せられると弱さを見せちゃうんだ。
→「やせ我慢」より「愛情」が強い
でも「愛情」も「小切手」を見せられると心が揺らいじゃうよ。
→「愛情」より「小切手」が強い
ただ、「小切手」を見せられたとしても「やせ我慢」で耐えられるんだ。
→「小切手」より「やせ我慢」が強い

■　クライアント作成のポイント
1. サーバに接続
2. ルールを受信して表示
3.キーボードから入力した0～2の数字のどれかを送る
4.サーバ側で計算された勝負結果が送られてくる
（以後、勝負の繰り返し）
※「3」を送るとゲーム終了となり、最終成績が送られてくる

ちなみに「3」を送るまではずっとゲームが続く神仕様だよ！
'''

print(MESSAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()

while True:
    sock_c, addr = sock.accept()

    threading.Thread(target=janken, args=(sock_c, addr)).start()

sock.close()