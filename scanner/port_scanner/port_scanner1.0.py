"""
端口扫描器1.0，单线程
python port_scanner1.0.py 127.0.0.1 0-1023
"""

import sys
from socket import *


target_host=sys.argv[1]
target_ip=gethostbyname(target_host)

from_port=int(sys.argv[2].split('-')[0])
to_port=int(sys.argv[2].split('-')[1])

for port in range(from_port,to_port+1):
    s=socket(AF_INET,SOCK_STREAM)
    s.settimeout(2)
    res=s.connect_ex((target_ip,port))
    if res==0:
        print(port)
print("done")