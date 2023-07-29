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
from modules.invite import *
from modules.getId import *
from modules.sortByDistance import *
from modules.buildTeam import *

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
teams = {}


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
        invites = useSql(f"SELECT * FROM invites WHERE user2='{user}' AND showed=0 AND allowed=0 LIMIT 1")
        if invites:
            invite = invites[0]
            data = useSql(f"SELECT * FROM users WHERE username='{invite[1]}'")[0]
            distance = getDistance(data[1], user)
            size = useSql(f"SELECT * FROM inSearch WHERE username='{data[1]}'")[0][7]
            if distance:
                caption = f'Есть возможность погулять с этим человеком:\n\nИмя: {data[2]}\nПол: {data[4]}\nВозраст: {data[6]} лет\nГород: {data[7]}\nРазмер компании: {size}📍 {distance[0]} {distance[1]}'
            else:
                caption = f'Есть возможность погулять с этим человеком:\n\nИмя: {data[2]}\nПол: {data[4]}\nВозраст: {data[6]} лет\nГород: {data[7]}\nРазмер компании: {size}'

            await bot.send_photo(mess.chat.id, photo=data[3], caption=caption, reply_markup=ikb_allow)
            useSql(f"DELETE FROM invites WHERE user2='{user}'")
            useSql(f"INSERT INTO invites (id, user1, user2, showed, allowed) VALUES ({invite[0]}, '{invite[1]}', '{invite[2]}', 1, 0)")

        await asyncio.sleep(1)


@dp.callback_query_handler(lambda c: c.data == 'allow')
async def send_random_value(callback: types.CallbackQuery):
    username = getId(callback)
    data = useSql(f"SELECT * FROM invites WHERE user2='{username}' LIMIT 1")[0]
    useSql(f"DELETE FROM invites WHERE id={data[0]}")
    useSql(f"INSERT INTO invites (id, user1, user2, showed, allowed) VALUES ({data[0]}, '{data[1]}', '{data[2]}', 1, 1)")

@dp.callback_query_handler(lambda c: c.data == 'reject')
async def send_random_value(callback: types.CallbackQuery):
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
        await message.reply('Я вижу, что ты впервые здесь, давай создадим анкету.\nКак тебя зовут?')
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

async def getUser(mess, username, username2=None):
    data = useSql(f"SELECT * FROM users WHERE username='{username}'")[0]
    if username2:
        distance = getDistance(username, username2)
    else:
        distance = None
    await card(mess, data, distance)


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

    elif mess.text == 'В главное меню':
        await mess.reply('Главное меню:', reply_markup=kb_menu)
        await reset(mess, getId(mess))

    elif mess.text == 'пошел нахер':
        await mess.reply('сам такой', reply_markup=kb_menu)

    elif mess.text == 'Покинуть компанию':
        await mess.reply('Вы покинули компанию', reply_markup=kb_menu)
        await reset(mess, getId(mess))

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

                await bot.send_message(mess.chat.id, 'Идет поиск...', reply_markup=kb_exit)
                count = int(mess.text)
                userdata = useSql(f"SELECT * FROM users WHERE username='{getId(mess)}'")[0]
                if useSql(f"SELECT username FROM inSearch WHERE username='{getId(mess)}'"):
                    useSql(f"DELETE FROM inSearch WHERE username='{getId(mess)}'")

                useSql(f"INSERT INTO inSearch (username, city, age, genre, anotherGenre, approved, count, coordinates, chatId) VALUES ('{getId(mess)}', '{userdata[7]}', '{userdata[6]}', '{userdata[4]}', '{userdata[5]}', '[]', {count}, '{userdata[8]}', {mess.chat.id})")
                await findTeam(mess)

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
    # if not(useSql("SELECT * FROM inSearch WHERE username='Mot05112'")):
    #     useSql("INSERT INTO inSearch (username, city, age, genre, anotherGenre, approved, count, coordinates) VALUES ('Mot05112', 'Киров', 14, 'Мужской', 'Мужской', '[]', 3, '[56.084518, 56.680753]')")
    # if not(useSql("SELECT * FROM inSearch WHERE username='l1'")):
    #     useSql("INSERT INTO inSearch (username, city, age, genre, anotherGenre, approved, count, coordinates) VALUES ('l1', 'Киров', 14, 'Мужской', 'Женский', '[]', 2, '[56.084518, 56.680753]')")
    # if not(useSql("SELECT * FROM inSearch WHERE username='l2'")):
    #     useSql("INSERT INTO inSearch (username, city, age, genre, anotherGenre, approved, count, coordinates) VALUES ('l2', 'Киров', 14, 'Женский', 'Не важно', '[]', 3, '[]')")
    # if not(useSql("SELECT * FROM inSearch WHERE username='l3'")):
    #     useSql("INSERT INTO inSearch (username, city, age, genre, anotherGenre, approved, count, coordinates) VALUES ('l3', 'Киров', 14, 'Женский', 'Женский', '[]', 3, '[]')")
    # if not(useSql("SELECT * FROM inSearch WHERE username='l4'")):
    #     useSql("INSERT INTO inSearch (username, city, age, genre, anotherGenre, approved, count, coordinates) VALUES ('l4', 'Киров', 14, 'Женский', 'Мужской', '[]', 2, '[56.084518, 56.680753]')")

    loop = asyncio.get_event_loop()
    loop.create_task(teaming())
    executor.start_polling(dp, skip_updates=True)