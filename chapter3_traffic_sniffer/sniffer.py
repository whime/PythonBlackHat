import socket
import os

"""
a simple demo of sniffer
"""
targetHost = "127.0.0.1"

if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)
sniffer.bind((targetHost,0))

sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

# windows promiscuous mode on
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)
while True:
    print(sniffer.recvfrom(65535))
# windows promiscuous mode off
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)

