# Net-Cut
С помощью данной консольной утилиты вы можете отключить интернет пользователю, зная его локальный IP адрес

## Зависимости
Требуется установить:
- `python3-pip` 
- `git`
- `libnfnetlink-dev`
- `libnetfilter-queue-dev`

Далее нужно установить `netfilterqueue`:<br>
`pip install -U git+https://github.com/kti/python-netfilterqueue`

## Запуск:
Запускать приложение нужно с правами супер пользователя
`sudo ./main.py <ip-адрес>`

```
usage: net-cut [-h] [-w] ip

С помощью данной консольной утилиты вы можете отключить интернет пользователю, зная
его локальный IP адрес

positional arguments:
  ip             IP пользователя, которого нужно отключить от сети

options:
  -h, --help     show this help message and exit
  -w, --waiting  Ждать ли пользователя, после его отключения от сети (по умолчанию: нет)
```