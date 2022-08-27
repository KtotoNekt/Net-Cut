# Net-Cut
С помощью данной консольной утилиты вы можете отключить интернет пользователю, зная его локальный IP адресс

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
`sudo python main.py <ip-адресс>`