import asyncio
import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram import Bot, Dispatcher,types
from aiogram.types import Message
import sqlite3 as sq

TOKEN = "5721458659:AAEPnYmZTy4LJap8M__AngXbyGj7ZwSRFjo"
bot = Bot(TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    name = State()
    faculty = State()
    course = State()
    group = State()
    # even_odd = State()


def request_to_user_db(sql):
    with sq.connect("rasp.db") as con:  # подключение к базе данных
        cur = con.cursor()  # создание объекта для работы с базой данных
        cur.execute(sql)
        result = cur.fetchall()
        return result

def check_user(mes):
    sql = 'SELECT tg_id FROM users'
    check = request_to_user_db(sql)
    a = []
    for res in check:
        for x in res:
            a.append(x)
    if mes.chat.id in a:
        return 2
    else:
        return 1

def save_user(mes,data):
    print(data)
    result = []
    for res in data:
        result.append(data[res])
    firstname = result[0].split()[0]
    secondname = result[0].split()[1]
    with sq.connect("rasp.db") as con:  # подключение к базе данных
        cur = con.cursor()  # создание объекта для работы с базой данных
        cur.execute("""INSERT INTO users (tg_id,firstname,secondname,faculty,course,groupnumber) VALUES (?,?,?,?,?,?)""",(mes.chat.id, firstname, secondname,str(result[1]),int(result[2]),int(result[3])))

def rasp(mes, num):
    user_result = request_to_user_db(f'SELECT * FROM users WHERE tg_id = {mes.chat.id}')
    rasp_result = request_to_user_db(f'SELECT * FROM rasper WHERE faculty == "{user_result[0][4]}" AND course == {user_result[0][5]} AND numbergroup == {user_result[0][6]} AND evenoddweek == {num}')
    rasp = []
    for x in rasp_result:
        rasp.append(x[4])
        rasp.append(x[5])
        rasp.append(x[10])
        rasp.append(x[12])
    message = f'Понедельник:\n{rasp[0]} - {rasp[1]}\n{rasp[3]}\n{rasp[0]} - {rasp[1]}\n{rasp[3+4]}\n{rasp[0]} - {rasp[1]}\n{rasp[3+8]}\n\n' \
              f'Вторник:\n{rasp[0]} - {rasp[1]}\n{rasp[15]}\n{rasp[0]} - {rasp[1]}\n{rasp[15+4]}\n{rasp[0]} - {rasp[1]}\n{rasp[15+8]}\n\n' \
              f'Среда:\n{rasp[0]} - {rasp[1]}\n{rasp[27]}\n{rasp[0]} - {rasp[1]}\n{rasp[27+4]}\n{rasp[0]} - {rasp[1]}\n{rasp[27+8]}\n\n' \
              f'Четверг:\n{rasp[0]} - {rasp[1]}\n{rasp[43]}\n{rasp[0]} - {rasp[1]}\n{rasp[43+4]}\n{rasp[0]} - {rasp[1]}\n{rasp[43+8]}\n\n' \
              f'Пятница:\n{rasp[0]} - {rasp[1]}\n{rasp[51]}\n{rasp[0]} - {rasp[1]}\n{rasp[51+4]}\n{rasp[0]} - {rasp[1]}\n{rasp[51+8]}\n\n'
    return message


@dp.message_handler(commands=["start"])
async def command_start_handler(message: Message) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = f"Профиль"
    item2 = f"Расписание"
    markup.add(item1, item2)
    await bot.send_message(message.chat.id, 'Добро пожаловать!\nЧем могу помочь?', reply_markup=markup)

@dp.message_handler()
async def message_handler(message: types.Message):
    if message.text.lower() == 'расписание':
        check = check_user(message)
        if check == 1:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('Регистрация','Назад')
            await bot.send_message(message.chat.id, 'Вам нужно зарегестрироваться', reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('Четная','Нечетная','Назад')
            await bot.send_message(message.chat.id, 'Какую неделю хотите посмотреть?',reply_markup=markup)

    if message.text.lower() == 'четная':
        a = 2
        await bot.send_message(message.chat.id, rasp(message, a))
    if message.text.lower() == 'нечетная':
        a = 1
        await bot.send_message(message.chat.id, rasp(message, a))

    if message.text.lower() == 'профиль':
        check = check_user(message)
        if check == 1:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('Регистрация','Назад')
            await bot.send_message(message.chat.id, 'Вам нужно зарегестрироваться', reply_markup=markup)
        else:
            result = request_to_user_db(f'SELECT * FROM users WHERE tg_id == {message.chat.id}')
            mes = f'{result[0][2]} {result[0][3]}\nФакультет: {result[0][4]}\nКурс: {result[0][5]}\nГруппа: {result[0][6]}'
            await bot.send_message(message.chat.id, mes)
    if message.text.lower() == 'назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Профиль','Расписание')
        await bot.send_message(message.chat.id, 'Добро пожаловать!\nЧем могу помочь?', reply_markup=markup)

    if message.text.lower() == 'регистрация':
        check = check_user(message)
        if check == 2:
            await bot.send_message(message.chat.id, 'Вы уже зарегестрированы!')
        else:
            await Form.name.set()
            a = types.ReplyKeyboardRemove()
            await bot.send_message(message.chat.id, "Напишите своё имя и фамилию\nПример: Магомед Магомедов\n\nДля отмены напишите /cancel", reply_markup=a)

@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Профиль', 'Расписание')
    if current_state is None:
        return
    await state.finish()
    await message.reply('Операция отменена', reply_markup=markup)

@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    items = ['ИФМиТО','БГиХ','ДО','ДФ','ИСТ','ИЯ','МП','НК','СПиП','УиП','ФКиБЖ','ХГ','ФИЯ',]
    for item in items:
        markup.add(item)
    await Form.next()
    await message.reply("С какого ты факультета?", reply_markup=markup)

@dp.message_handler(lambda message: message.text, state=Form.faculty)
async def process_age(message: types.Message, state: FSMContext):
    items = ['ИФМиТО', 'БГиХ', 'ДО', 'ДФ', 'ИСТ', 'ИЯ', 'МП', 'НК', 'СПиП', 'УиП', 'ФКиБЖ', 'ХГ', 'ФИЯ', ]
    if message.text not in items:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Профиль', 'Расписание')
        await state.finish()
        await bot.send_message(message.chat.id,'Выберите факультет из списка!', reply_markup=markup)
    else:
        async with state.proxy() as data:
            data['faculty'] = message.text
        await Form.next()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        items = ['1', '2', '3', '4', '5']
        for item in items:
            markup.add(item)
        await message.reply("На каком вы курсе?", reply_markup=markup)

@dp.message_handler(lambda message: message.text, state=Form.course)
async def process_age(message: types.Message, state: FSMContext):
    a = 0
    try:
        message.text = int(message.text)
    except ValueError:
        await state.finish()
        a = 1
    if a == 1:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Профиль', 'Расписание')
        await bot.send_message(message.chat.id, 'Выберите курс из списка!', reply_markup=markup)
    num = [1, 2, 3, 4, 5]
    if message.text not in num:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Профиль', 'Расписание')
        await state.finish()
        await bot.send_message(message.chat.id, 'Выберите курс из списка!', reply_markup=markup)
    else:
        async with state.proxy() as data:
            data['course'] = message.text
        await Form.next()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        items = ['1', '2', '3', '4']
        for item in items:
            markup.add(item)
        await message.reply("В какой вы группе??", reply_markup=markup)

@dp.message_handler(lambda message: message.text, state=Form.group)
async def process_age(message: types.Message, state: FSMContext):
    a = 0
    try:
        message.text = int(message.text)
    except ValueError:
        await state.finish()
        a = 1
    if a == 1:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Профиль', 'Расписание')
        await bot.send_message(message.chat.id, 'Выберите группу из списка!', reply_markup=markup)
    num = [1, 2, 3, 4]
    if message.text not in num:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Профиль', 'Расписание')
        await state.finish()
        await bot.send_message(message.chat.id, 'Выберите группу из списка!', reply_markup=markup)
    else:
        async with state.proxy() as data:
            data['group'] = message.text
        await state.finish()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Профиль', 'Расписание')
        await bot.send_message(message.chat.id, 'Регистрация прошла успешно!', reply_markup=markup)
        save_user(message, data)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())