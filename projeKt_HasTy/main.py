import telebot
import requests

from telebot.async_telebot import AsyncTeleBot
import asyncio
import aiohttp

import sqlite3 as sq #При желании убрать
def add_user(id): #Эта функция здесь по сути не нужна, добавлена с целью сбора tg.id, можно закоментировать
    sql = f"INSERT INTO users (tg_id) VALUES({id})"
    with sq.connect("users.db") as con:
        cur = con.cursor()
        cur.execute(sql)

bot = AsyncTeleBot("5721458659:AAEPnYmZTy4LJap8M__AngXbyGj7ZwSRFjo")

def weather(): #Подключаемся к API и забираем данные
    response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=42.98&longitude=47.50&hourly=temperature_2m")
    return response

def split_day(): #Отделяем от даты ненужные значения, оставляем только day
    time = weather().json()['hourly']['time']
    ints_list = []
    for i in range(len(time)):
        ints_list.append(str(time[i].lower()[8:-6]))
    day = []
    for x in ints_list:
        if x not in day:
            day.append(x)
    return day

def temperature(num): #Высчитываем значения температуры для дней
    temp = weather().json()['hourly']['temperature_2m']
    len_temp = []
    if num  == 0:
        len_temp.append(temp[8])
        len_temp.append(temp[15])
        len_temp.append(temp[21])
    elif num  == 1:
        len_temp.append(temp[32])
        len_temp.append(temp[39])
        len_temp.append(temp[45])
    elif num  == 2:
        len_temp.append(temp[56])
        len_temp.append(temp[63])
        len_temp.append(temp[69])
    elif num  == 3:
        len_temp.append(temp[80])
        len_temp.append(temp[87])
        len_temp.append(temp[93])
    elif num  == 4:
        len_temp.append(temp[104])
        len_temp.append(temp[111])
        len_temp.append(temp[117])
    elif num  == 5:
        len_temp.append(temp[128])
        len_temp.append(temp[135])
        len_temp.append(temp[141])
    elif num  == 6:
        len_temp.append(temp[152])
        len_temp.append(temp[159])
        len_temp.append(temp[165])
    return len_temp

@bot.message_handler(commands=['start'])
async def start_message(message):
    add_user(message.chat.id)
    day = split_day()
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = []
    for i in range(7):
        item.append(telebot.types.KeyboardButton(f"{day[i]} число"))
    markup.add('Сегодня', 'Завтра', item[2], item[3],item[4],item[5],item[6])
    await bot.send_message(message.chat.id, 'Выберите день на который вам нужна погода', reply_markup=markup)

@bot.message_handler(content_types=['text'])
async def get_text_messages(message):
    number = split_day()
    if message.text.lower() == "сегодня":
        temp = temperature(0)
        await bot.send_message(message.chat.id, f'☁Погода на сегодня☁\nУтро: {int(temp[0])}°C\nДень: {int(temp[1])}°C\nВечер: {int(temp[2])}°C')
    elif message.text.lower() == "завтра":
        temp = temperature(1)
        await bot.send_message(message.chat.id, f'☁Погода на завтра☁\nУтро: {int(temp[0])}°C\nДень: {int(temp[1])}°C\nВечер: {int(temp[2])}°C')
    elif message.text.lower() == f"{number[2]} число":
        temp = temperature(2)
        await bot.send_message(message.chat.id, f'☁Погода на {number[2]} число☁\nУтро: {int(temp[0])}°C\nДень: {int(temp[1])}°C\nВечер: {int(temp[2])}°C')
    elif message.text.lower() == f"{number[3]} число":
        temp = temperature(3)
        await bot.send_message(message.chat.id, f'☁Погода на {number[3]} число☁\nУтро: {int(temp[0])}°C\nДень: {int(temp[1])}°C\nВечер: {int(temp[2])}°C')
    elif message.text.lower() == f"{number[4]} число":
        temp = temperature(4)
        await bot.send_message(message.chat.id, f'☁Погода на {number[4]} число☁\nУтро: {int(temp[0])}°C\nДень: {int(temp[1])}°C\nВечер: {int(temp[2])}°C')
    elif message.text.lower() == f"{number[5]} число":
        temp = temperature(5)
        await bot.send_message(message.chat.id, f'☁Погода на {number[5]} число☁\nУтро: {int(temp[0])}°C\nДень: {int(temp[1])}°C\nВечер: {int(temp[2])}°C')
    elif message.text.lower() == f"{number[6]} число":
        temp = temperature(6)
        await bot.send_message(message.chat.id, f'☁Погода на {number[6]} число☁\nУтро: {int(temp[0])}°C\nДень: {int(temp[1])}°C\nВечер: {int(temp[2])}°C')

asyncio.run(bot.infinity_polling())