"""
dict 服务端部分
处理请求逻辑
"""

from socket import *
from multiprocessing import Process
import signal
import sys
import time
from operation_db import *

# 全局变量
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)

# 处理注册 R name passwd
def do_register(c,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    if db.register(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'FAIL')

# 处理登录 L name passwd
def do_login(c,db,data):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    if db.login(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'FAIL')

# 处理查询 Q name word
def do_query(c,db,data):
    l = data.split(' ')
    name = l[1]
    word = l[2]
    # 插入历史记录
    db.insert_history(name,word)
    # 查单词 没有查到返回None
    mean = db.query(word)
    if not mean:
        c.send('没有找到该单词'.encode())
    else:
        msg = "%s : %s"%(word,mean)
        c.send(msg.encode())

# 处理历史记录 H name
def do_history(c,db,data):
    l = data.split(' ')
    name = l[1]
    # 查询10条历史记录
    r = db.history(name)
    if not r:
        c.send(b'FAIL')
        return

    c.send(b'OK')
    for i in r:
        # i -> (name,word,time)
        msg = '%s %s %s'%i
        time.sleep(0.1) # 防止粘包
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b'##')

# 处理客户端请求
def do_request(c,db):
    db.create_cursor() # 生成游标
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername(),':',data)
        if not data or data[0] == 'E':
            #db.close()
            c.close()
            sys.exit('客户端退出')#退出子进程
        elif data[0] == 'R':
            do_register(c,db,data)
        elif data[0] == 'L':
            do_login(c,db,data)
        elif data[0] == 'Q':
            do_query(c,db,data)
        elif data[0] == 'H':
            do_history(c,db,data)

# 网络连接
def main():
    # 创建数据库连接对象
    db = Database()

    # 创建tcp套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    # 等待客户端连接
    while True:
        try:
            c,addr = s.accept()
            print("Connect from:",addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit('服务器退出')
        except Exception as e:
            print('Failed:',e)
            continue

        # 创建子进程
        p = Process(target=do_request,args=(c,db))
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()