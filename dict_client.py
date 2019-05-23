"""
dict 客户端部分
发起请求，展示结果
"""

from socket import *
from getpass import getpass

ADDR = ('127.0.0.1',8000)

s = socket()
s.connect(ADDR)

# 二级界面
# name需要告诉服务端是谁在查单词、谁在查历史记录
def login(name):
    while True:
        print("""
        ========Query========
        1.查单词
        2.历史记录
        3.注销
        =====================
        """)
        cmd = input("请输入选项:")
        if cmd == '1':
            do_register()
        elif cmd == '2':
            do_login()
        elif cmd == '3':
            return
        else:
            print("请输入正确命令")

# 注册
def do_register():
    while True:
        name = input("请输入用户名:")
        passwd = getpass("请输入密码:")
        passwd1 = getpass("请再次输入密码:")

        if (' ' in name) or (' ' in passwd):
            print("用户名或密码里不能有空格")
            continue

        if passwd != passwd1:
            print("两次密码不一致")
            continue

        msg = "R %s %s"%(name,passwd)
        # 发送请求
        s.send(msg.encode())
        # 接收反馈
        data = s.recv(128).decode()
        if data == 'OK':
            print("注册成功")
            login(name)# 进入二级界面
        else:
            print("注册失败")
        return
# 登录
def do_login():
    name = input("请输入用户名:")
    passwd = getpass("请输入密码:")

    if (' ' in name) or (' ' in passwd):
        print("用户名或密码里不能有空格")
        return

    msg = "L %s %s"%(name,passwd)
    s.send(msg.encode())
    # 等待反馈
    data = s.recv(128).decode()
    if data == 'OK':
        print("登录成功")
        login(name)# 进入二级界面
    else:
        print("登录失败")

# 退出
def do_exit():
    pass

# 创建网络连接
def main():
    while True:
        print("""
        =======welcome=======
        1.注册
        2.登录
        3.退出
        =====================
        """)
        cmd = input("请输入选项:")
        if cmd == '1':
            do_register()
        elif cmd == '2':
            do_login()
        elif cmd == '3':
            do_exit()
        else:
            print("请输入正确命令")

if __name__ == '__main__':
    main()