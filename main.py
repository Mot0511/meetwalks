from aiogram import *
from aiogram.types import *
from modules.useSql import useSql
from modules.getDistance import *
import time
import asyncio
import json
import random
from geopy.geocoders import Nominatim
from modules.keyboards import *
from itertools import groupby
from modules.statistics import *
from modules.getId import *
from modules.sortByDistance import *
from modules.buildTeam import *
from modules.getUsers import *

api_token = open('token_test.txt', 'r').read()
bot = Bot(token=api_token)

dp = Dispatcher(bot)

action = {}
isEditing = {}

name = {}
photo = {}
genre = {}
age = {}
city = {}
coordinates = {}

applicants = {}
counts = {}

teams = {}
teamIds = {}


async def findAllowed(user, chat):
    while True:
        invites = useSql(f"SELECT * FROM invites WHERE user1='{user}'")
        if invites:
            for i in invites:
                if i[4] == 1:
                    await bot.send_message(chat, 'Пользователь '+i[2]+' принял')
                    useSql(f"DELETE FROM invites WHERE id={i[0]}")
                    useSql(f"INSERT INTO invites (id, user1, user2, showed, allowed) VALUES ({i[0]}, '{i[1]}', '{i[2]}', 1, 2)")

                elif i[4] == -1:
                    await bot.send_message(chat, 'Пользователь ' + i[2] + ' отклонил')
                    useSql(f"DELETE FROM invites WHERE id={i[0]}")
                    useSql(f"INSERT INTO invites (id, user1, user2, showed, allowed) VALUES ({i[0]}, '{i[1]}', '{i[2]}', 1, 2)")
        else:
            return

        await asyncio.sleep(1)

async def findInvites(mess, user):
    while True:
        invites = json.loads(useSql(f"SELECT invites FROM users WHERE username='{user}'")[0][0])
        if invites:
            inviter = invites[0]
            users = json.loads(useSql(f"SELECT members FROM teams WHERE id='{teamIds[inviter]}'")[0][0])
            await bot.send_message(mess.chat.id, 'Есть возможность погулять с этими людьми:')
            users.remove(user)
            for i in users:
                print(users)
                data = useSql(f"SELECT * FROM users WHERE username='{i}'")[0]
                distance = getDistance(data[1], user)
                size = counts[inviter]
                if distance:
                    caption = f'\n\nИмя: {data[2]}\nПол: {data[4]}\nВозраст: {data[6]} лет\nГород: {data[7]}\nРазмер компании: {size}📍 {distance[0]} {distance[1]}'
                else:
                    caption = f'\n\nИмя: {data[2]}\nПол: {data[4]}\nВозраст: {data[6]} лет\nГород: {data[7]}\nРазмер компании: {size}'

                await bot.send_photo(mess.chat.id, photo=data[3], caption=caption, reply_markup=kb_allow)
                useSql(f"UPDATE users SET invites='[]' WHERE username='{user}'")

        await asyncio.sleep(1)


@dp.callback_query_handler(lambda c: c.data == 'allow')
async def allow(callback: types.CallbackQuery):
    username = getId(callback)
    data = useSql(f"SELECT invites FROM users WHERE ")[0]
    useSql(f"")

@dp.callback_query_handler(lambda c: c.data == 'reject')
async def reject(callback: types.CallbackQuery):
    username = getId(callback)
    data = useSql(f"SELECT * FROM invites WHERE user2='{username}' LIMIT 1")[0]
    useSql(f"DELETE FROM invites WHERE id={data[0]}")
    useSql(f"INSERT INTO invites (id, user1, user2, showed, allowed) VALUES ({data[0]}, '{data[1]}', '{data[2]}', 1, -1)")



j = 0
async def teaming():
    while True:
        global j
        people = useSql("SELECT * FROM inSearch")
        team = []
        if not(people == []):
            if len(people) - 1 < j:
                j = 0
            inSearchData = people[j]
            # print(':'+inSearchData[1]+':')
            userdata = useSql(f"SELECT * FROM users WHERE username='{inSearchData[1]}'")[0]# getting userdata
            count = inSearchData[7]

            if not(userdata[8] == '[]'):
                if userdata[5] == 'Не важно':
                    data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND anotherGenre='Не важно' AND NOT username='{userdata[1]}' AND count={count} AND NOT coordinates='[]' LIMIT {count - 1};")
                    if data == []:
                        data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[4]}' AND genre=anotherGenre AND NOT username='{userdata[1]}' AND count={count} AND NOT coordinates='[]' LIMIT {count - 1};")
                else:
                    data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND anotherGenre='{userdata[4]}' AND NOT username='{userdata[1]}' AND count={count} AND NOT coordinates='[]' LIMIT {count - 1};")
                    if data == []:
                        data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND anotherGenre='Не важно' AND NOT username='{userdata[1]}' AND count={count} AND NOT coordinates='[]' LIMIT {count - 1};")
                if not(data == []):
                    data = sortByDistance(inSearchData[1], data)
                    for i in data:
                        team.append(i[1])

                    team = [el for el, _ in groupby(team)]
                    if len(team) == count - 1:
                        await buildTeam(team, inSearchData[1])
                        await teaming()

                    else:
                        remainder = count - len(team)
                        if userdata[5] == 'Не важно':
                            data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[4]}' AND genre=anotherGenre AND NOT username='{userdata[1]}' AND count={count} AND NOT coordinates='[]' LIMIT {remainder - 1};")
                        else:
                            data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND anotherGenre='Не важно' AND NOT username='{userdata[1]}' AND count={count} AND NOT coordinates='[]' LIMIT {remainder - 1};")
                        data = sortByDistance(inSearchData[1], data)
                        for i in data:
                            team.append(i[1])

                        team = [el for el, _ in groupby(team)]
                        if len(team) == count - 1:
                            await buildTeam(team, inSearchData[1])
                            await teaming()

            remainder = count - len(team)
            if userdata[5] == 'Не важно':
                data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND anotherGenre='Не важно' AND NOT username='{userdata[1]}' AND coordinates='[]' AND count={count} LIMIT {remainder - 1};")
                if data == []:
                    data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[4]}' AND genre=anotherGenre AND NOT username='{userdata[1]}' AND count={count} AND coordinates='[]' LIMIT {remainder - 1};")

            else:
                data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND anotherGenre='{userdata[4]}' AND NOT username='{userdata[1]}' AND coordinates='[]' AND count={count} LIMIT {remainder - 1};")
                if data == []:
                    data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND anotherGenre='Не важно' AND NOT username='{userdata[1]}' AND count={count} AND coordinates='[]' LIMIT {remainder - 1};")

            if not(data == []):
                for i in data:
                    team.append(i[1])

            team = [el for el, _ in groupby(team)]
            if len(team) == count - 1:
                await buildTeam(team, inSearchData[1])
                await teaming()

            else:
                remainder = count - len(team)
                if userdata[5] == 'Не важно':
                    data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[4]}' AND genre=anotherGenre AND NOT username='{userdata[1]}' AND count={count} AND coordinates='[]' LIMIT {remainder - 1};")
                else:
                    data = useSql(f"SELECT * FROM inSearch WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND anotherGenre='Не важно' AND NOT username='{userdata[1]}' AND count={count} AND coordinates='[]' LIMIT {remainder - 1};")
                for i in data:
                    team.append(i[1])

                team = [el for el, _ in groupby(team)]
                if len(team) == count - 1:
                    await buildTeam(team, inSearchData[1])
                    await teaming()
                else:
                    if not(useSql(f"SELECT user1 FROM invites WHERE user1='{inSearchData[1]}'")):
                        invite(inSearchData[1], userdata[6], count, userdata[4], userdata[5], userdata[7], (None, userdata[8])[bool(userdata[8])])
                        loop = asyncio.get_event_loop()
                        chatId = useSql(f"SELECT chatId FROM inSearch WHERE username='{userdata[1]}'")[0][0]
                        loop.create_task(findAllowed(userdata[1], chatId))

        j += 1
        await asyncio.sleep(1)

async def findTeam(mess):
    while True:
        if useSql(f"SELECT * FROM inSearch WHERE username='{getId(mess)}'"):
            await asyncio.sleep(2)
            if getId(mess) in teams:
                await bot.send_message(mess.chat.id, 'Компания сформирована:', reply_markup=kb_leave)
                teamId = teams[getId(mess)]
                members = json.loads(useSql(f"SELECT members FROM teams WHERE id={teamId}")[0][0])
                members.remove(getId(mess))
                for member in members:
                    await getUser(mess, member, getId(mess))

                global action
                action[getId(mess)] = 'chat'
                await bot.send_message(mess.chat.id, 'Общий чат:', reply_markup=kb_leave)
                while getId(mess) in teams:
                    username = useSql(f"SELECT * FROM users WHERE username='{getId(mess)}'")[0][2]
                    oldChat = json.loads(useSql(f"SELECT chat FROM teams WHERE id={teamId}")[0][0])
                    await asyncio.sleep(0.5)
                    newChat = json.loads(useSql(f"SELECT chat FROM teams WHERE id={teamId}")[0][0])
                    if not(oldChat == newChat):
                        for i in oldChat:
                            if i in newChat:
                                newChat.remove(i)

                        for i in newChat:
                            if i[0] == username:
                                newChat.remove(i)

                        for i in newChat:
                            await bot.send_message(mess.chat.id, f'{i[0]}: {i[1]}', reply_markup=kb_leave)
                break
        else:
            break
    return

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global action
    data = useSql(f"SELECT * FROM users WHERE username='{getId(message)}'")
    if not(data):
        await message.reply('Meetwalks - это бот, в котором можно найти людей для прогулки в твоем городе')
        await message.reply('Я вижу, что ты впервые здесь, давай создадим анкету.\nКак тебя зовут?', reply_markup=types.ReplyKeyboardRemove())

        action[getId(message)] = 'setName'
    else:
        await message.reply('Meetwalks - это бот, в котором можно найти людей для прогулки в твоем городе', reply_markup=kb_menu)
        await findInvites(message, getId(message))

    await reset(message, getId(message), isAction=False)
@dp.message_handler(commands=['statistics'])
async def statistics(mess: types.Message):
    data = getStatistics()
    await mess.reply(data, reply_markup=kb_menu)

async def card(mess, data, distance=None, keyboard=kb_menu):
    if distance == None:
        caption = f'Имя: {data[2]}\nПол: {data[4]}\nВозраст: {data[6]} лет\nГород: {data[7]}\n'
    else:
        caption = f'Имя: {data[2]}\nПол: {data[4]}\nВозраст: {data[6]} лет\nГород: {data[7]}\n📍 {distance[0]} {distance[1]}'


    await bot.send_photo(mess.chat.id, photo=data[3], caption=caption, reply_markup=keyboard)

async def reset(mess, user, isAction=True):
    useSql(f"DELETE FROM inSearch WHERE username='{user}'")
    useSql(f"DELETE FROM invites WHERE user1='{user}'")
    if user in teams:
        useSql(f"DELETE FROM teams WHERE id='{teams[user]}'")

    global applicants
    if getId(mess) in applicants:
        del applicants[getId(mess)]
    if getId(mess) in teams:
        del teams[getId(mess)]

    if isAction:
        global action
        action[getId(mess)] = ''

async def getUser(mess, username, username2=None, vote=False, keyboard=None):
    data = useSql(f"SELECT * FROM users WHERE username='{username}'")[0]
    if username2:
        distance = getDistance(username, username2)
    else:
        distance = None

    if keyboard:
        await card(mess, data, distance, keyboard=keyboard)
    else:
        await card(mess, data, distance)

async def find(mess):
    username = getId(mess)
    users = getUsers(username, counts[username])

    if users:
        await bot.send_message(mess.chat.id, 'Вам подходят эти люди:')
        for i in users:
            await getUser(mess, i, getId(mess), keyboard=kb_allow_team)
        teams[getId(mess)] = users
    else:
        await bot.send_message(mess.chat.id, 'Пока нет подходящих для вас людей')

@dp.message_handler()
async def text(mess: types.Message):
    loop = asyncio.get_event_loop()
    loop.create_task(findInvites(mess, getId(mess)))
    global action
    global genre
    global messTool
    global username
    username = getId(mess)
    if mess.text == 'Искать людей':
        userdata = useSql(f"SELECT * FROM users WHERE username='{getId(mess)}'")[0]
        kb = kb_count
        if not(userdata[5] == 'Не важно') and not(userdata[4] == userdata[5]):
            kb = kb_count

        await mess.reply('Сколько людей должно быть в компании?', reply_markup=kb)
        action[getId(mess)] = 'count'

    elif mess.text == 'Моя анкета':
        data = useSql(f"SELECT * FROM users WHERE username='{getId(mess)}'")[0]
        await card(mess, data, keyboard=kb_edit)

    elif mess.text == 'Изменить анкету':
        global isEditing
        isEditing[getId(mess)] = True
        await mess.reply('Как тебя зовут?', reply_markup=types.ReplyKeyboardRemove())
        action[getId(mess)] = 'setName'

    elif mess.text == 'В главное меню' or mess.text == 'Покинуть компанию':
        await mess.reply('Главное меню:', reply_markup=kb_menu)
        await reset(mess, getId(mess))

    elif mess.text == 'пошел нахер':
        await mess.reply('сам такой', reply_markup=kb_menu)

    elif mess.text == '✔':
        allowAppl[getId(mess)].append(applicants[getId(mess)])

    elif mess.text == '✖':
        allowAppl[getId(mess)].append(applicants[getId(mess)])

    elif mess.text == 'Поиск заново':
        await find(mess)

    elif mess.text == 'Одобрить компанию':
        for i in teams[getId(mess)]:
            invites = json.loads(useSql(f"SELECT invites FROM users WHERE username='{i}'")[0][0])
            invites.append(getId(mess))
            invites = json.dumps(invites)
            useSql(f"UPDATE users SET invites='{invites}' WHERE username='{i}'")

        teamId = random.randint(0, 1000)
        team = teams[getId(mess)]
        team.append(getId(mess))
        useSql(f"INSERT INTO teams (id, members, chat, allowed, owner, ready, count) VALUES ({teamId}, '{json.dumps(team)}', '[]', '[]', '{getId(mess)}', 0, {counts[getId(mess)]})")
        teamIds[getId(mess)] = teamId
        await bot.send_message(mess.chat.id, 'Ожидаем одобрения членов компании...')

    else:
        if getId(mess) in action:
            if action[getId(mess)] == 'chat':
                teamId = teams[getId(mess)]
                team = useSql(f"SELECT * FROM teams WHERE id='{teamId}'")[0]
                username = useSql(f"SELECT * FROM users WHERE username='{getId(mess)}'")[0][2]
                chat = json.loads(team[2])
                chat.append([username, mess.text])
                chat = json.dumps(chat)
                useSql(f"DELETE FROM teams WHERE id='{teamId}'")
                useSql(f"INSERT INTO teams (id, members, chat) VALUES ({teamId}, '{team[1]}', '{chat}')")

            elif action[getId(mess)] == 'count':
                new('search')
                if mess.text == 'Главное меню':
                    await mess.reply('Главное меню:', reply_markup=kb_menu)
                    await reset(mess, getId(mess))
                    return

                count = int(mess.text)
                counts[getId(mess)] = count
                await find(mess)

            elif action[getId(mess)] == 'setName':
                global name
                name[getId(mess)] = mess.text
                await mess.reply('Какой у тебя пол', reply_markup=kb_genre)
                action[getId(mess)] = 'setGenre'

            elif action[getId(mess)] == 'setGenre':
                genre[getId(mess)] = mess.text
                await mess.reply('Сколько тебе лет?', reply_markup=types.ReplyKeyboardRemove())
                action[getId(mess)] = 'setAge'

            elif action[getId(mess)] == 'setAge':
                global age
                age[getId(mess)] = mess.text
                await mess.reply('В каком городе ты живёшь?\n\nТакже ты можешь отправить свою геолокацию, чтобы подобрать наиболее близких по расположению людей', reply_markup=kb_sendLocation)
                action[getId(mess)] = 'setCity'

            elif action[getId(mess)] == 'setCity':
                global city
                city[getId(mess)] = mess.text
                await mess.reply('Теперь отправь свое фото')
                action[getId(mess)] = 'setPhoto'

            elif action[getId(mess)] == 'setAnotherGenre':
                global coordinates
                if getId(mess) in isEditing:
                    useSql(f"DELETE FROM users WHERE username='{getId(mess)}'")
                else:
                    new('users')

                if getId(mess) in coordinates:
                    useSql(f"INSERT INTO users (username, name, photo, genre, anotherGenre, age, city, coordinates) VALUES ('{getId(mess)}', '{name[getId(mess)]}', '{photo[getId(mess)]}', '{genre[getId(mess)]}', '{mess.text}', '{age[getId(mess)]}', '{city[getId(mess)]}', '{json.dumps(coordinates[getId(mess)])}')")
                else:
                    useSql(f"INSERT INTO users (username, name, photo, genre, anotherGenre, age, city, coordinates) VALUES ('{getId(mess)}', '{name[getId(mess)]}', '{photo[getId(mess)]}', '{genre[getId(mess)]}', '{mess.text}', '{age[getId(mess)]}', '{city[getId(mess)]}', '[]')")

                await mess.reply('Анкета готова', reply_markup=kb_menu)
                await findInvites(mess, getId(mess))
                isEditing[getId(mess)] = False
                action[getId(mess)] = 0

@dp.message_handler(content_types=['photo'])
async def getPhoto(mess: types.Message):
    global isEditing
    global action
    if action[getId(mess)] == 'setPhoto':
        global photo
        global useSql
        photo[getId(mess)] = mess.photo[-1].file_id
        await mess.reply('Какой пол ты хочешь находить?', reply_markup=kb_genre2)
        action[getId(mess)] = 'setAnotherGenre'

@dp.message_handler(content_types=['location'])
async def location(mess: types.Message):
    global coordinates
    global city
    global action
    coordinates[getId(mess)] = [mess.location.latitude, mess.location.longitude]
    geolocator = Nominatim(user_agent="Meetwalks")
    location = geolocator.reverse(f"{coordinates[getId(mess)][0]}, {coordinates[getId(mess)][1]}")
    city[getId(mess)] = location.address.split(', ')[-6]
    await mess.reply('Теперь отправь свое фото', reply_markup=types.ReplyKeyboardRemove())
    action[getId(mess)] = 'setPhoto'



if __name__ == '__main__':
    if not(useSql("SELECT * FROM users WHERE username='Mot05112'")):
        useSql("INSERT INTO users (username, name, photo, city, age, genre, anotherGenre, coordinates, invites) VALUES ('Mot05112', 'Пользователь7', 'AgACAgIAAxkBAANFZMD_2JbJdUG2Pfj5078xutZgDtsAAoTLMRtTywlKYfsUcoHV56IBAAMCAANtAAMvBA', 'Киров', 14, 'Мужской', 'Мужской', '[56.084518, 56.680753]', '[]')")
    if not(useSql("SELECT * FROM users WHERE username='l1'")):
        useSql("INSERT INTO users (username, name, photo, city, age, genre, anotherGenre, coordinates, invites) VALUES ('l1', 'Пользоатель3', 'AgACAgIAAxkBAANFZMD_2JbJdUG2Pfj5078xutZgDtsAAoTLMRtTywlKYfsUcoHV56IBAAMCAANtAAMvBA', 'Киров', 14, 'Мужской', 'Женский', '[56.084518, 56.680753]', '[]')")
    if not(useSql("SELECT * FROM users WHERE username='l2'")):
        useSql("INSERT INTO users (username, name, photo, city, age, genre, anotherGenre, coordinates, invites) VALUES ('l2', 'Пользоатель4', 'AgACAgIAAxkBAANFZMD_2JbJdUG2Pfj5078xutZgDtsAAoTLMRtTywlKYfsUcoHV56IBAAMCAANtAAMvBA', 'Киров', 14, 'Женский', 'Не важно', '[]', '[]')")
    if not(useSql("SELECT * FROM users WHERE username='l3'")):
        useSql("INSERT INTO users (username, name, photo, city, age, genre, anotherGenre, coordinates, invites) VALUES ('l3', 'Пользоатель5', 'AgACAgIAAxkBAANFZMD_2JbJdUG2Pfj5078xutZgDtsAAoTLMRtTywlKYfsUcoHV56IBAAMCAANtAAMvBA', 'Киров', 14, 'Женский', 'Женский', '[]', '[]')")
    if not(useSql("SELECT * FROM users WHERE username='l4'")):
        useSql("INSERT INTO users (username, name, photo, city, age, genre, anotherGenre, coordinates, invites) VALUES ('l4', 'Пользоатель6', 'AgACAgIAAxkBAANFZMD_2JbJdUG2Pfj5078xutZgDtsAAoTLMRtTywlKYfsUcoHV56IBAAMCAANtAAMvBA', 'Киров', 14, 'Женский', 'Мужской', '[56.084518, 56.680753]', '[]')")

    loop = asyncio.get_event_loop()
    # loop.create_task(teaming())
    executor.start_polling(dp, skip_updates=True)