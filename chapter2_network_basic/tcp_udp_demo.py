import socket
from multiprocessing import Process
import time
import os

"""
网络编程极简示例
"""


def TCPsocket():
    target_port = 80
    target_host = "www.baidu.com"
    # 创建套接字并连接,请求百度首页
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))
    # 发送请求
    client.send(b"GET / HTTP/1.1\r\nHost:baidu.com\r\n\r\n")

    html = ""

    while True:
        response = client.recv(1024).decode()
        if response:
            html += response
            print(response)
        else:
            break
    print("ok")
    client.close()

    # 将响应写入文件
    with open("baidu.html", 'w', encoding="utf8") as f:
        f.write(html)


# 开启一个UDP服务器
def startAnUdpServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', 10000))
    print('UDP server start at port 10000...')
    print("udp server pid:", os.getpid())
    data, addr = s.recvfrom(1024)
    print('udp server had receive something')
    s.sendto(b"Hello," + bytes(addr[0], encoding='utf8') + b",I receive " + data, addr)
    s.close()


def UDPsocket():
    # UDP客户端示例代码
    target_port = 10000
    target_host = "127.0.0.1"

    # 由于全局解释器锁的存在，同一个程序里面只能使用多进程，无法使用多线程
    # t=Thread(target=startAUdpServer())
    # t.start()
    p = Process(target=startAnUdpServer)
    p.start()

    # 等待子进程创建好socket
    time.sleep(10)
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # UDP无需连接
    client.sendto(b"AAABBBCCC", (target_host, target_port))

    data, addr = client.recvfrom(4096)
    print(data.decode())
    client.close()


if __name__ == '__main__':
    # TODO(whime) :tcp 执行起来很慢，待解决
    # TCPsocket()
    UDPsocket()
