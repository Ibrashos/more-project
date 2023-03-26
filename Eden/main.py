from telebot.async_telebot import AsyncTeleBot
import asyncio
import aiohttp
import telebot
import sqlite3 as sq
from operator import itemgetter
API_TOKEN = '5721458659:AAEPnYmZTy4LJap8M__AngXbyGj7ZwSRFjo'
bot = AsyncTeleBot(API_TOKEN)#add token

def request_to_user_db(sql):
    with sq.connect("user.db") as con:  # подключение к базе данных
        cur = con.cursor()  # создание объекта для работы с базой данных
        cur.execute(sql)
        result = cur.fetchall()
        print(result)
        return result

def add_user(mes):
    sql = 'SELECT tg_id FROM users'
    check = request_to_user_db(sql)
    if mes.chat.id in check:
        return 'У вас уже есть профиль'
    else:
        print(list(map(itemgetter(2, 3), mes.text)))
        sql = """INSERT INTO users (tg_id,firstname,secondname) VALUES (?,?,?)""", (mes.chat.id, name[0], name[1])
        # print(res)
        return 'Регистрация прошла успешно!'
# def look_user():

@bot.message_handler(commands=['start'])
async def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = (telebot.types.KeyboardButton(f"Профиль"))
    item2 = (telebot.types.KeyboardButton(f"Расписание"))
    markup.add(item1,item2)
    await bot.send_message(message.chat.id, 'Добро пожаловать!\nЧем могу помочь?', reply_markup=markup)


@bot.message_handler(content_types=['text'])
async def get_text_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text.lower() == 'профиль':
        sql = 'SELECT tg_id FROM users'
        # request_to_db()
        markup.add('Регистрация')
        await bot.send_message(message.chat.id, 'У вас ещё нет профиля, вам нужно зарегестрироваться', reply_markup=markup)
    elif message.text.lower() == 'регистрация':
        # await bot.send_message(message.chat.id, "Введите своё Имя и фамилию\nПример: Магомед Магомедов")
        response = await bot.wait_for(message.chat.id, "Введите своё Имя и фамилию\nПример: Магомед Магомедов")
        await bot.send_message(message.chat.id, response.text)
        add_user(message)






asyncio.run(bot.infinity_polling())


