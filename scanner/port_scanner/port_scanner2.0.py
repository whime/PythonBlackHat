"""
端口扫描器2.0，多线程
python port_scanner2.0.py 127.0.0.1 1000-2000
"""

from threading import Thread,Lock
from socket import *
import sys

target_host = sys.argv[1]
target_ip = gethostbyname(target_host)
threadLock=Lock()

def scan(port):
    sock=socket(AF_INET,SOCK_STREAM)
    sock.settimeout(10)
    res=sock.connect_ex((target_ip,port))
    if res==0:
        threadLock.acquire()
        print(port)
        threadLock.release()


if __name__ == '__main__':
    from_port=int(sys.argv[2].split('-')[0])
    to_port=int(sys.argv[2].split('-')[1])
    threadList=[]
    for port in range(from_port,to_port+1):
        t=Thread(target=scan,args=(port,))
        threadList.append(t)
    for t in threadList:
        t.start()
    print("done")

