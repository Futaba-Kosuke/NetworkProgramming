import multiprocessing

print('a')

def f(mesg):
    print('b')

print('c')

if __name__ == '__main__':
    print('d')
    multiprocessing.Process(target=f, args=('test', )).start()
    print('e')

print('f')
