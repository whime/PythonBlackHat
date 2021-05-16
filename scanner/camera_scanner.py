#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import ipaddress
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp
import re
import requests


"""
@author:whime
@description:scan the potential camera in local network
"""
class camera_scanner:
    def __init__(self, net, timeout=4,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}):
        self.target_net = net
        self.timeout = timeout
        self.headers=headers

    def scan(self):
        try:
            network = ipaddress.ip_network(self.target_net, strict=False)
            print("start to scan network " + str(network) + "...")
        except ValueError as e:
            print(e)
        else:
            packet = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=self.target_net)
            # TODO(需要一个获取当前使用的网卡的方法作为全局变量）
            # TODO(有个缺陷，对于使用随机地址的设备来说，无法获取其真实mac地址）
            ans, _ = srp(packet, iface="Realtek PCIe GBE Family Controller", timeout=self.timeout)
            print("there is/are %d machine(s) in %s"%(len(ans),str(network)))
            # print(ans.summary())

            for s, r in ans:
                mac = r[ARP].hwsrc
                inqueryUrl = "https://mac.bmcx.com/{0}__mac/".format(mac)
                try:
                    res=requests.get(inqueryUrl,headers=self.headers)
                    pattern=re.compile('style="font-size:16px;">(.*?)</td>',re.S)
                    result=re.findall(pattern,res.text)[1]
                    print(mac+"=>"+result)
                except Exception:
                    print("error in query mac address,maybe a random address: "+mac)

                finally:
                    pass


if __name__ == '__main__':
    scanner = camera_scanner("192.168.1.1/24")
    scanner.scan()
