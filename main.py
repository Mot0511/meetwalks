from aiogram import *
from aiogram.types import *
import sqlite3 as sq
import time
import asyncio
import threading
import json
import random

api_token = open('token.txt', 'r').read()
bot = Bot(token=api_token)
dp = Dispatcher(bot)
conn = sq.connect('db.db')

kb_genre = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('Мужской'), KeyboardButton('Женский'))
kb_genre2 = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('Мужской'), KeyboardButton('Женский'), KeyboardButton('Не важно'))
kb_menu = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('Искать людей'), KeyboardButton('Моя анкета'))
kb_edit = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('Изменить анкету'), KeyboardButton('В главное меню'))
kb_select = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('✔'), KeyboardButton('✖')).add(KeyboardButton('В главное меню'))
kb_exit = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('В главное меню'))
kb_leave = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Покинуть команду'))
action = ''
isEditing = False

name = ''
photo = ''
genre = ''
age = 0
city = ''
coordinates = 0.0

applicants = {}
teams = {}
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global action
    data = useSql(f"SELECT * FROM users WHERE username='{message.from_user.username}'")
    if not(data):
        await message.reply('Meetwalks - это бот, в котором можно найти людей для прогулки в твоем городе')
        await message.reply('Я вижу, что ты впервые здесь, давай создадим анкету.\nКак тебя зовут?')
        action = 'setName'
    else:
        await message.reply('Meetwalks - это бот, в котором можно найти людей для прогулки в твоем городе', reply_markup=kb_menu)

def useSql(q):
    cur = conn.cursor()
    cur.execute(q)
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data

async def card(mess, data, keyboard=kb_select):
    caption = f'Имя: {data[2]}\nПол: {data[4]}\nВозраст: {data[6]} лет\nГород: {data[7]}'
    await bot.send_photo(mess.chat.id, photo=data[3], caption=caption, reply_markup=keyboard)


async def search(mess):
    global applicants
    approved = check_approve(mess)
    if approved:
        data = useSql(f"SELECT * FROM users WHERE username='{approved[0]}'")[0]
        await card(mess, data)
        applicants[mess.from_user.username] = approved[0]
        approved.pop(0)
        approved = json.dumps(approved)
        userdata = useSql(f"SELECT * FROM users WHERE username='{mess.from_user.username}'")[0]
        useSql(f"DELETE FROM inSearch WHERE username='{mess.from_user.username}'")
        useSql(f"INSERT INTO inSearch (username, city, age, genre, anotherGenre, approved) VALUES ('{mess.from_user.username}', '{userdata[7]}', '{userdata[6]}', '{userdata[4]}', '{userdata[5]}', '{approved}')")
    else:
        userdata = useSql(f"SELECT * FROM users WHERE username='{mess.from_user.username}'")[0]
        if userdata[5] == 'Не важно':
            data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND NOT username='{userdata[1]}' ORDER BY RANDOM() LIMIT 1;")
        else:
            data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND NOT username='{userdata[1]}' ORDER BY RANDOM() LIMIT 1;")

        if data == []:
            await asyncio.sleep(2)
            await search(mess)
        else:
            applicant = useSql(f"SELECT * FROM users WHERE username='{data[0][1]}'")[0]
            await card(mess, applicant)
            applicants[mess.from_user.username] = data[0][1]

async def getUser(mess, username):
    if useSql(f"EXISTS(SELECT username FROM inSearch WHERE username='{username}')"):
        data = useSql(f"SELECT * FROM users WHERE username='{username}'")[0]
        await card(mess, data)


def check_approve(mess):
    data = useSql(f"SELECT * FROM inSearch WHERE username='{mess.from_user.username}'")[0]
    if data[6]:
        return json.loads(data[6])
    else:
        return None

@dp.message_handler()
async def text(mess: types.Message):
    global action
    global genre
    global messTool
    if mess.text == 'Искать людей':
        userdata = useSql(f"SELECT * FROM users WHERE username='{mess.from_user.username}'")[0]
        if not(useSql(f"SELECT username FROM inSearch WHERE username='{mess.from_user.username}'")):
            useSql(f"INSERT INTO inSearch (username, city, age, genre, anotherGenre, approved) VALUES ('{mess.from_user.username}', '{userdata[7]}', '{userdata[6]}', '{userdata[4]}', '{userdata[5]}', '[]')")
        await mess.reply('Идет поиск...', reply_markup=kb_exit)
        await search(mess)

    elif mess.text == 'Моя анкета':
        data = useSql(f"SELECT * FROM users WHERE username='{mess.from_user.username}'")[0]
        await card(mess, data, kb_edit)

    elif mess.text == 'Изменить анкету':
        global isEditing
        isEditing = True
        await mess.reply('Как тебя зовут?', reply_markup=types.ReplyKeyboardRemove())
        action = 'setName'

    elif mess.text == 'В главное меню':
        await mess.reply('Главное меню:', reply_markup=kb_menu)
        useSql(f"DELETE FROM inSearch WHERE username='{mess.from_user.username}'")

    elif mess.text == 'пошел нахер':
        await mess.reply('сам такой', reply_markup=kb_menu)

    elif mess.text == 'Покинуть команду':
        useSql(f"DELETE FROM teams WHERE id='{teams[mess.from_user.username]}'")
        global applicants
        del applicants[mess.from_user.username]
        await mess.reply('Вы покинули компанию', reply_markup=kb_menu)


    elif mess.text == '✔':
        if json.loads(useSql(f"SELECT * FROM inSearch WHERE username='{mess.from_user.username}'")[0][6]).count(applicants[mess.from_user.username]) > 0:
            useSql(f"DELETE FROM inSearch WHERE username='{mess.from_user.username}'")
            useSql(f"DELETE FROM inSearch WHERE username='{applicants[mess.from_user.username]}'")
            teamId = random.randint(0, 10000)
            useSql(f"INSERT INTO teams (id, members) VALUE ('{teamId}', '[\"{mess.from_user.username}\", \"{applicants[mess.from_user.username]}\"]')")
            teams[mess.from_user.username] = teamId
            teams[applicants[mess.from_user.username]] = teamId
            await bot.send_message(f'Ваша компания:\n\n{mess.from_user.username}\n{applicants[mess.from_user.username]}', reply_markup=kb_leave)
        else:
            approved = useSql(f"SELECT * FROM inSearch WHERE username='{applicants[mess.from_user.username]}'")[0][6]
            approved = json.loads(approved)
            approved.append(mess.from_user.username)
            approved = json.dumps(approved).replace("'", '"')
            userdata = useSql(f"SELECT * FROM users WHERE username='{applicants[mess.from_user.username]}'")[0]
            useSql(f"DELETE FROM inSearch WHERE username='{applicants[mess.from_user.username]}'")
            useSql(f"INSERT INTO inSearch (username, city, age, genre, anotherGenre, approved) VALUES ('{applicants[mess.from_user.username]}', '{userdata[7]}', '{userdata[6]}', '{userdata[4]}', '{userdata[5]}', '{approved}')")
            del applicants[mess.from_user.username]

    elif mess.text == '✖':
        await search(mess)

    else:
        if action == 'setName':
            global name
            name = mess.text
            await mess.reply('Какой у тебя пол', reply_markup=kb_genre)
            action = 'setGenre'

        elif action == 'setGenre':
            genre = mess.text
            await mess.reply('Сколько тебе лет?', reply_markup=types.ReplyKeyboardRemove())
            action = 'setAge'

        elif action == 'setAge':
            global age
            age = mess.text
            await mess.reply('В каком городе ты живёшь?')
            action = 'setCity'

        elif action == 'setCity':
            global city
            city = mess.text
            await mess.reply('Теперь отправь свое фото')
            action = 'setPhoto'

        elif action == 'setAnotherGenre':
            global anotherGenre
            anotherGenre = mess.text
            try:
                if isEditing:
                    useSql(f"DELETE FROM users WHERE username='{mess.from_user.username}'")

                useSql(
                    f"INSERT INTO users (username, name, photo, genre, anotherGenre, age, city, coordinates) VALUES ('{mess.from_user.username}', '{name}', '{photo}', '{genre}', '{anotherGenre}', '{age}', '{city}', '{coordinates}')")
                await mess.reply('Анкета готова', reply_markup=kb_menu)
                isEditing = False
                action = 0
            except sq.Error as error:
                await mess.reply('Ошибка создания анкеты, попробуйте позже')
                print(error)

@dp.message_handler(content_types=['photo'])
async def photo(mess: types.Message):
    global isEditing
    global action
    if action == 'setPhoto':
        global photo
        global useSql
        photo = mess.photo[-1].file_id
        await mess.reply('Какой пол ты хочешь оценивать?', reply_markup=kb_genre2)
        action = 'setAnotherGenre'




executor.start_polling(dp, skip_updates=True)