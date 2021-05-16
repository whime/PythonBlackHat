import socket
import os
import struct
from ctypes import *
from netaddr import IPAddress, IPNetwork
import threading
import time

"""
A scanner sending udp package with specific message to the subnet,
wait for network machine alive to respond with ICMP (type 3,code 3)
"""
host = "192.168.29.1"
subnet = "192.168.29.0/24"


class IP(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4),
        ("version", c_ubyte, 4),  # big-endian
        ("tos", c_ubyte),
        ("len", c_ushort),
        ("id", c_ushort),
        ("offset", c_ushort),
        ("ttl", c_ubyte),
        ("protocol_num", c_ubyte),
        ("sum", c_ushort),
        ("src", c_ulong),
        ("dst", c_ulong)
    ]

    def __new__(cls, socket_buffer=None):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}

        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except KeyError:
            self.protocol = str(self.protocol_num)


class ICMP(Structure):
    _fields_ = [
        ("type", c_ubyte),
        ("code", c_ubyte),
        ("checksum", c_ushort),
        ("unuse", c_ushort),
        ("next_hop_mtu", c_ushort),
    ]

    def __new__(cls, socket_buffer):
        return cls.from_buffer_copy(socket_buffer)

    def __init__(self, _):
        pass


def main():
    if os.name == "nt":
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    specific_msg = "python".encode("utf8")

    def udp_sender(net, msg):
        time.sleep(5)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        for ip in IPNetwork(net):
            try:
                sock.sendto(msg, ("%s" % ip, 65212))
            except Exception as e:
                print(e)
                pass
    t = threading.Thread(target=udp_sender,args=(subnet,specific_msg))
    t.start()

    try:
        while True:
            raw_data = sniffer.recvfrom(65565)[0]
            ip_header = IP(raw_data[:20])
            # print("protocol %s:%s ->%s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))

            if ip_header.protocol == "ICMP":
                icmp_offset = ip_header.ihl * 4
                buf = raw_data[icmp_offset:icmp_offset + sizeof(ICMP)]

                ICMP_header = ICMP(buf)
                print(ip_header.src_address, ICMP_header.type)
                # print("ICMP ->type:%d,code:%d" % (ICMP_header.type, ICMP_header.code))
                if IPAddress(ip_header.src_address) in IPNetwork(subnet):
                    # print(ip_header.src_address, ICMP_header.type)
                    if ICMP_header.type == 3 and ICMP_header.code == 3:
                        print(ip_header.src_address)
                        if raw_data[len(raw_data)-len(specific_msg):] == specific_msg:
                            print("Host up:%s"%ip_header.src_address)

    except KeyboardInterrupt:
        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


if __name__ == '__main__':
    main()
