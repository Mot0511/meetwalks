from aiogram import *
from aiogram.types import *
import sqlite3 as sq
import time
import asyncio

api_token = open('token.txt', 'r').read()
bot = Bot(token=api_token)
dp = Dispatcher(bot)
conn = sq.connect('db.db')

kb_genre = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('Мужской'), KeyboardButton('Женский'))
kb_genre2 = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('Мужской'), KeyboardButton('Женский'), KeyboardButton('Не важно'))
kb_menu = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('Искать людей'), KeyboardButton('Моя анкета'))
kb_edit = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('Изменить анкету'), KeyboardButton('В главное меню'))

kb_select = ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton('✔'), KeyboardButton('✖')).add(KeyboardButton('В главное меню'))

action = ''
isEditing = False

name = ''
photo = ''
genre = ''
age = 0
city = ''
coordinates = 0.0

genre_search = ''

async def searchTimer():
    await asyncio.sleep(2)
    search_task = asyncio.create_task(search())
    await search_task

def useSql(q):
    cur = conn.cursor()
    cur.execute(q)
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data

async def search():
    userdata = useSql(f"SELECT * FROM users WHERE username='{messTool.from_user.username}'")[0]
    if genre_search == 'Не важно':
        data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[5]} + 2) AND age > ({userdata[5]} - 2)) AND city='{userdata[6]}' AND NOT username='{userdata[1]}' ORDER BY RANDOM() LIMIT 1;")
    else:
        data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[5]} + 2) AND age > ({userdata[5]} - 2)) AND city='{userdata[6]}' AND genre='{genre_search}' AND NOT username='{userdata[1]}' ORDER BY RANDOM() LIMIT 1;")

    print(data)
    if data == []:
        await search()
    else:
        data = data[0]
        global applicant
        applicant = useSql(f"SELECT * FROM users WHERE username='{data[1]}'")[0]
        caption = f'Имя: {applicant[2]}\nПол: {applicant[4]}\nВозраст: {applicant[5]} лет\nГород: {applicant[6]}'
        await bot.send_photo(messTool.chat.id, photo=applicant[3], caption=caption, reply_markup=kb_select)



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


@dp.message_handler()
async def text(mess: types.Message):
    global action
    global genre
    global messTool
    if mess.text == 'Искать людей':
        await mess.reply('Пол искаемого человека:', reply_markup=kb_genre2)
        action = 'search'


    elif mess.text == 'Моя анкета':
        data = useSql(f"SELECT * FROM users WHERE username='{mess.from_user.username}'")[0]
        caption = f'Имя: {data[2]}\nПол: {data[4]}\nВозраст: {data[5]} лет\nГород: {data[6]}'
        await bot.send_photo(mess.chat.id, photo=data[3], caption=caption, reply_markup=kb_edit)

    elif mess.text == 'Изменить анкету':
        global isEditing
        isEditing = True
        await mess.reply('Как тебя зовут?', reply_markup=types.ReplyKeyboardRemove())
        action = 'setName'

    elif mess.text == 'В главное меню':
        await mess.reply('Главное меню:', reply_markup=kb_menu)

    elif mess.text == '✔':
        print(applicant)

    elif mess.text == '✖':
        messTool = mess
        search_task = asyncio.create_task(search())
        await search_task

    else:
        if action == 'setName':
            global name
            name = mess.text
            await mess.reply('Какой у тебя пол', reply_markup=kb_genre)
            action = 'setGenre'

        elif action == 'search':
            await mess.reply('Идет поиск...')
            genre = mess.text
            userdata = useSql(f"SELECT * FROM users WHERE username='{mess.from_user.username}'")[0]
            useSql(f"INSERT INTO inSearch (username, city, age, genre, approved) VALUES ('{mess.from_user.username}', '{userdata[6]}', '{userdata[5]}', '{userdata[4]}', '')")
            time.sleep(2)
            data = useSql(f"SELECT * FROM inSearch WHERE username='{mess.from_user.username}'")[0]
            if data[5]:
                print(1)
            else:
                global userdata_search
                global genre_search
                genre_search = genre
                messTool = mess
                await search()



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

@dp.message_handler(content_types=['photo'])
async def photo(mess: types.Message):
    global isEditing
    global action
    if action == 'setPhoto':
        global photo
        global useSql
        photo = mess.photo[-1].file_id
        try:
            if isEditing:
                useSql(f"DELETE FROM users WHERE username='{mess.from_user.username}'")
                useSql(f"INSERT INTO users (username, name, photo, genre, age, city, coordinates) VALUES ('{mess.from_user.username}', '{name}', '{photo}', '{genre}', '{age}', '{city}', '{coordinates}')")
            else:
                useSql(f"INSERT INTO users (username, name, photo, genre, age, city, coordinates) VALUES ('{mess.from_user.username}', '{name}', '{photo}', '{genre}', '{age}', '{city}', '{coordinates}')")
            await mess.reply('Анкета готова', reply_markup=kb_menu)
            isEditing = False
            action = 0
        except sq.Error as error:
            await mess.reply('Ошибка создания анкеты, попробуйте позже')
            print(error)

executor.start_polling(dp, skip_updates=True)