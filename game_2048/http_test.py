from socket import *
from os import *
import sys

# 服务器地址
ADDR = ('127.0.0.1', 8888)
# 发送消息
def send_msg(s, name):
    while True:
        text = input("发言：")
        msg = 'C %s %s' % (name, text)
        s.sendto(msg.encode(), ADDR)
# 接收消息
def recv_msg(s):
    while True:
        data, addr = s.recvfrom(1024)
        print(data.decode())
# 客户端启动函数
def main():
    s = socket(AF_INET, SOCK_DGRAM)
    # 进入聊天室
    while True:
        name = input("请输入姓名：")
        msg = "L " + name
        s.sendto(msg.encode(), ADDR)
        # 接受反馈
        data, addr = s.recvfrom(128)
        if data.decode() == 'OK':
            print("您已进入聊天室")
            break
        else:
            print(data.decode())
    pid = os.fork()
    if pid < 0:
        sys.exit("ERROR!")
    elif pid == 0:
        send_msg(s, name)  # 子进程负责消息发送
    else:
        recv_msg(s)  # 父进程负责消息接受

main()