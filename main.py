from aiogram import *
from aiogram.types import *
import sqlite3 as sq
import time
import asyncio
import threading
import json
import random
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from modules.keyboards import *

api_token = open('token.txt', 'r').read()
bot = Bot(token=api_token)
dp = Dispatcher(bot)
conn = sq.connect('db.db')

action = ''
isEditing = False

name = ''
photo = ''
genre = ''
age = 0
city = ''
coordinates = []

applicants = {}
teams = {}

def useSql(q):
    cur = conn.cursor()
    cur.execute(q)
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return data

async def buildTeam(team, username):
    global teams
    team.append(username)
    teamId = random.randint(0, 10000)
    for i in team:
        teams[i] = teamId
        useSql(f"DELETE FROM inSearch WHERE username='{i}'")

    print('Team: '+team)
    team = json.dumps(team).replace("'", '"')
    useSql(f"INSERT INTO teams (id, members) VALUES ('{teamId}', '{team}')")
    # print('Team was created')
    print(teams)


async def teaming():
    # print('Start loop of searching')
    people = useSql("SELECT * FROM inSearch")
    team = [] # our team
    if not(people == []):
        # print('First person has gotten')
        inSearchData = people[0] # getting inSearch data
        userdata = useSql(f"SELECT * FROM users WHERE username='{inSearchData[1]}'")[0] # getting userdata
        count = inSearchData[7] # getting count of members
        # print('Checking for the presence of coordinates')
        # checking for the presence of coordinates
        if not(userdata[8] == '[]'):
            # print('Getting people with the coordinates')
            # getting people with the coordinates
            if userdata[5] == 'Не важно':
                data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND NOT username='{userdata[1]}' AND count={count} AND NOT coordinates='[]'")
            else:
                data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND NOT username='{userdata[1]}' AND count={count} AND NOT coordinates='[]'")

            # print('Checking for the presence people with coordinates')
            # checking for the presence people with coordinates
            if not(data == []):
                # ---------- sort by descending distance
                # print('Creating team')
                if len(data) < count - 1:
                    for i in data:
                        team.append(i[1])
                else:
                    for i in range(count - 1):
                        team.append(data[i][1])

                if len(team) == count:
                    await buildTeam(team, inSearchData[1])
        # print('Getting people without the coordinates')
        # getting people without the coordinates
        if userdata[5] == 'Не важно':
            data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND NOT username='{userdata[1]}' AND count={count}")
        else:
            data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND NOT username='{userdata[1]}' AND count={count}")

        if not(data == []):
            if len(data) >= count - 1:
                for i in range(count - 1):
                    team.append(data[i][1])

        if len(team) == count:
            await buildTeam(team, inSearchData[1])


    await asyncio.sleep(2)
    await teaming()

@dp.message_handler(commands=['s'])
async def start(message: types.Message):
    global action
    data = useSql(f"SELECT * FROM users WHERE username='{message.from_user.username}'")
    if not(data):
        await message.reply('Meetwalks - это бот, в котором можно найти людей для прогулки в твоем городе')
        await message.reply('Я вижу, что ты впервые здесь, давай создадим анкету.\nКак тебя зовут?')
        action = 'setName'
    else:
        await message.reply('Meetwalks - это бот, в котором можно найти людей для прогулки в твоем городе', reply_markup=kb_menu)

    await teaming()
    await reset(message, message.from_user.username)

async def card(mess, data, distance):
    if distance == None:
        caption = f'Имя: {data[2]}\nПол: {data[4]}\nВозраст: {data[6]} лет\nГород: {data[7]}\n'
    else:
        caption = f'Имя: {data[2]}\nПол: {data[4]}\nВозраст: {data[6]} лет\nГород: {data[7]}\n📍 {distance[0]} {distance[1]}'

    await bot.send_photo(mess.chat.id, photo=data[3], caption=caption)

async def reset(mess, user):
    useSql(f"DELETE FROM inSearch WHERE username='{user}'")
    if user in teams:
        useSql(f"DELETE FROM teams WHERE id='{teams[user]}'")

    global applicants
    if mess.from_user.username in applicants:
        del applicants[mess.from_user.username]
    if mess.from_user.username in teams:
        del teams[mess.from_user.username]

def getDistance(user, applicant):
    userCoordinates = json.loads(useSql(f"SELECT coordinates FROM users WHERE username='{user}'")[0][0])
    applicantCoordinates = json.loads(useSql(f"SELECT coordinates FROM users WHERE username='{applicant}'")[0][0])
    if userCoordinates and applicantCoordinates:
        distance = geodesic(userCoordinates, applicantCoordinates).km
        unit = 'км'
        if int(distance) == 0:
            distance *= 1000
            unit = 'м'

        return [int(distance), unit]

    return None

async def getUser(mess, username, username2=None):
    data = useSql(f"SELECT * FROM users WHERE username='{username}'")[0]
    distance = getDistance(username, username2)
    await card(mess, data, distance)


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
    global username
    username = mess.from_user.username
    if mess.text == 'Искать людей':
        print('\n')
        await mess.reply('Сколько людей должно быть в компании?', reply_markup=kb_count)
        action = 'count'

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
        await reset(mess, mess.from_user.username)

    elif mess.text == 'пошел нахер':
        await mess.reply('сам такой', reply_markup=kb_menu)

    elif mess.text == 'Покинуть компанию':
        await mess.reply('Вы покинули компанию', reply_markup=kb_menu)
        await reset(mess, mess.from_user.username)

    else:
        if action == 'count':
            if mess.text == 'Главное меню':
                await mess.reply('Главное меню:', reply_markup=kb_menu)
                await reset(mess, mess.from_user.username)
                return

            count = int(mess.text)
            userdata = useSql(f"SELECT * FROM users WHERE username='{mess.from_user.username}'")[0]
            if useSql(f"SELECT username FROM inSearch WHERE username='{mess.from_user.username}'"):
                useSql(f"DELETE FROM inSearch WHERE username='{mess.from_user.username}'")

            useSql(f"INSERT INTO inSearch (username, city, age, genre, anotherGenre, approved, count, coordinates) VALUES ('{mess.from_user.username}', '{userdata[7]}', '{userdata[6]}', '{userdata[4]}', '{userdata[5]}', '[]', {count}, '{userdata[8]}')")

            print('Start while loop')
            while True:
                await asyncio.sleep(2)
                if mess.from_user.username in teams:
                    print(mess.from_user.username+': Team formed')
                    await bot.send_message(mess.chat.id, 'Компания сформирована:', reply_markup=kb_leave)
                    teamId = teams[mess.from_user.username]
                    members = json.loads(useSql(f"SELECT members FROM teams WHERE id={teamId}")[0][0])
                    for member in members:
                        await getUser(mess, member, mess.from_user.username)

                    await bot.send_message(mess.chat.id, 'Общий чат:')
                    break


        elif action == 'setName':
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
            await mess.reply('В каком городе ты живёшь?\n\nТакже ты можешь отправить свою геолокацию, чтобы подобрать наиболее близких по расположению людей', reply_markup=kb_sendLocation)
            action = 'setCity'

        elif action == 'setCity':
            global city
            city = mess.text
            await mess.reply('Теперь отправь свое фото')
            action = 'setPhoto'

        elif action == 'setAnotherGenre':
            global coordinates
            global anotherGenre
            anotherGenre = mess.text
            try:
                if isEditing:
                    useSql(f"DELETE FROM users WHERE username='{mess.from_user.username}'")

                coordinates = json.dumps(coordinates)
                useSql(f"INSERT INTO users (username, name, photo, genre, anotherGenre, age, city, coordinates) VALUES ('{mess.from_user.username}', '{name}', '{photo}', '{genre}', '{anotherGenre}', '{age}', '{city}', '{coordinates}')")
                useSql(f"INSERT INTO users (username, name, photo, genre, anotherGenre, age, city, coordinates) VALUES ('{mess.from_user.username}', '{name}', '{photo}', '{genre}', '{anotherGenre}', '{age}', '{city}', '{coordinates}')")

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
        await mess.reply('Какой пол ты хочешь находить?', reply_markup=kb_genre2)
        action = 'setAnotherGenre'

@dp.message_handler(content_types=['location'])
async def location(mess: types.Message):
    global coordinates
    global city
    global action
    coordinates = [mess.location.latitude, mess.location.longitude]
    geolocator = Nominatim(user_agent="Meetwalks")
    location = geolocator.reverse(f"{coordinates[0]}, {coordinates[1]}")
    city = location.address.split(', ')[-6]
    await mess.reply('Теперь отправь свое фото', reply_markup=types.ReplyKeyboardRemove())
    action = 'setPhoto'

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(teaming())
    executor.start_polling(dp, skip_updates=True)