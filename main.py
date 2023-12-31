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

dev_mode = False

if dev_mode:
    api_token = open('token_test.txt', 'r').read()
    bot = Bot(token=api_token)
else:
    api_token = open('token.txt', 'r').read()
    bot = Bot(token=api_token, proxy='http://proxy.server:3128')

dp = Dispatcher(bot)

action = {}
isEditing = {}

name = {}
photo = {}
genre = {}
age = {}
city = {}
coordinates = {}

owners = {}
counts = {}
teams = {}
teamIds = {}
rejAppl = {}


@dp.message_handler(commands=['start', 's'])
async def start(message: types.Message):
    global action
    data = useSql(f"SELECT * FROM users WHERE username='{getId(message)}'")
    if not(data):
        await message.reply('Meetwalks - это бот, в котором можно найти людей для прогулки в твоем городе')
        await message.reply('Я вижу, что ты впервые здесь, давай создадим анкету.\nКак тебя зовут?', reply_markup=types.ReplyKeyboardRemove())

        action[getId(message)] = 'setName'
    else:
        await message.reply('Meetwalks - это бот, в котором можно найти людей для прогулки в твоем городе', reply_markup=kb_menu)


        if useSql(f"SELECT chatID FROM users WHERE username='{getId(message)}'")[0][0] == None:
            useSql(f"UPDATE users SET chatId={message.chat.id} WHERE username='{getId(message)}'")
            loop = asyncio.get_event_loop()
            loop.create_task(findInvites(message.chat.id, getId(message)))

        await reset(message, getId(message), isAction=False)

def getName(user):
    name = useSql(f"SELECT name FROM users WHERE username='{user}'")[0][0]
    return name
async def findInvites(chatId, user):
    while True:
        if not(useSql(f"SELECT username FROM users WHERE username='{user}'")):
            await asyncio.sleep(1)
            continue
        invites = json.loads(useSql(f"SELECT invites FROM users WHERE username='{user}'")[0][0])
        if invites:
            inviter = invites[0]
            users = json.loads(useSql(f"SELECT members FROM teams WHERE id='{teamIds[inviter]}'")[0][0])
            await bot.send_message(chatId, 'Есть возможность погулять с этими людьми:')
            users.remove(user)
            for i in users:
                data = useSql(f"SELECT * FROM users WHERE username='{i}'")[0]
                distance = getDistance(data[1], user)
                size = counts[inviter]
                if distance:
                    caption = f'\n\n@{data[1]}\nИмя: {data[2]}\nПол: {data[4]}\nВозраст: {data[6]} лет\nГород: {data[7]}\nРазмер компании: {size}\n📍 {distance[0]} {distance[1]}'
                else:
                    caption = f'\n\n@{data[1]}\nИмя: {data[2]}\nПол: {data[4]}\nВозраст: {data[6]} лет\nГород: {data[7]}\nРазмер компании: {size}'

                await bot.send_photo(chatId, photo=data[3], caption=caption, reply_markup=kb_allow)
                owners[user] = inviter
                useSql(f"UPDATE users SET invites='[]' WHERE username='{user}'")

        await asyncio.sleep(1)

async def findTeam(mess):
    while True:
        if getId(mess) in teamIds:
            owner = owners[getId(mess)]
            teamData = useSql(f"SELECT members, allowed, rejects FROM teams WHERE owner='{owner}'")[0]
            allowed = json.loads(teamData[1])
            members = json.loads(teamData[0])
            rejects = json.loads(teamData[2])
            rejUsers = ''
            if len(members) - 1 == len(allowed) + len(rejects):
                if len(members) - 1 == len(rejects):
                    await bot.send_message(mess.chat.id, 'Никто не принял заявку в компанию(', reply_markup=kb_menu)
                    useSql(f"DELETE FROM teams WHERE owner='{owner}'")
                    return

                if rejects:
                    rejUsers = ' (кроме: '
                    for i in rejects:
                        name = getName(i)
                        rejUsers += name+','
                    rejUsers += ')'

                await bot.send_message(mess.chat.id, f'Компания сформирована{("", rejUsers)[bool(rejUsers)]}:', reply_markup=kb_leave)
                teamId = teamIds[owner]
                members = json.loads(useSql(f"SELECT members FROM teams WHERE id={teamId}")[0][0])
                members.remove(getId(mess))
                for member in members:
                    if not(member in rejects):
                        await getUser(mess, member, getId(mess), keyboard=kb_leave)

                global action
                action[getId(mess)] = 'chat'
                await bot.send_message(mess.chat.id, 'Общий чат:', reply_markup=kb_leave)
                while getId(mess) in teamIds:
                    username = getId(mess)
                    oldChat = json.loads(useSql(f"SELECT chat FROM teams WHERE id={teamId}")[0][0])
                    oldRejects = json.loads(useSql(f"SELECT rejects FROM teams WHERE id={teamId}")[0][0])
                    await asyncio.sleep(0.3)
                    newChat = json.loads(useSql(f"SELECT chat FROM teams WHERE id={teamId}")[0][0])
                    newRejects = json.loads(useSql(f"SELECT rejects FROM teams WHERE id={teamId}")[0][0])
                    if not (oldRejects == newRejects):
                        for i in oldRejects:
                            if i in newRejects:
                                newRejects.remove(i)

                        for i in newRejects:
                            if i == username:
                                newRejects.remove(i)

                        for i in newRejects:
                            name = getName(i)
                            await bot.send_message(mess.chat.id, f'_{name} покинул(а) компанию_', reply_markup=kb_leave, parse_mode="Markdown")

                    if not (oldChat == newChat):
                        for i in oldChat:
                            if i in newChat:
                                newChat.remove(i)

                        for i in newChat:
                            if i[0] == username:
                                newChat.remove(i)

                        for i in newChat:
                            name = getName(i[0])
                            await bot.send_message(mess.chat.id, f'{name}: {i[1]}', reply_markup=kb_leave)
        else:
            return

        await asyncio.sleep(2)

@dp.message_handler(commands=['statistics'])
async def statistics(mess: types.Message):
    data = getStatistics()
    await mess.reply(data, reply_markup=kb_menu)

async def card(mess, data, distance=None, keyboard=kb_menu):
    if distance == None:
        caption = f'@{data[1]}\nИмя: {data[2]}\nПол: {data[4]}\nВозраст: {data[6]} лет\nГород: {data[7]}\n'
    else:
        caption = f'@{data[1]}\nИмя: {data[2]}\nПол: {data[4]}\nВозраст: {data[6]} лет\nГород: {data[7]}\n📍 {distance[0]} {distance[1]}'

    await bot.send_photo(mess.chat.id, photo=data[3], caption=caption, reply_markup=keyboard)

async def reset(mess, user, isAction=True):
    global owners
    global action
    if getId(mess) in owners:
        del owners[getId(mess)]
    if getId(mess) in teams:
        del teams[getId(mess)]
    if getId(mess) in teamIds:
        del teamIds[getId(mess)]
    if getId(mess) in counts:
        del counts[getId(mess)]
    if getId(mess) in rejAppl:
        del rejAppl[getId(mess)]


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
    if getId(mess) in rejAppl:
        users = getUsers(username, counts[username], rejAppl[getId(mess)])
    else:
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
    if useSql(f"SELECT chatID FROM users WHERE username='{getId(mess)}'")[0][0] == None:
        useSql(f"UPDATE users SET chatId={mess.chat.id} WHERE username='{getId(mess)}'")
        loop = asyncio.get_event_loop()
        loop.create_task(findInvites(mess.chat.id, getId(mess)))

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
        if mess.text == 'Покинуть компанию':
            data = useSql(f"SELECT rejects, count FROM teams WHERE owner='{owners[getId(mess)]}'")[0]
            rejects = json.loads(data[0])
            count = data[1]
            rejects.append(getId(mess))
            useSql(f"UPDATE teams SET rejects='{json.dumps(rejects)}' WHERE owner='{owners[getId(mess)]}'")
            if len(rejects) == count:
                useSql(f"DELETE FROM teams WHERE owner='{owners[getId(mess)]}'")


        await mess.reply('Главное меню:', reply_markup=kb_menu)
        await reset(mess, getId(mess))

    elif mess.text == 'Принять':
        owner = owners[getId(mess)]
        teamData = useSql(f"SELECT id, allowed FROM teams WHERE owner='{owner}'")[0]
        teamId = teamData[0]
        allowed = json.loads(teamData[1])
        allowed.append(getId(mess))
        useSql(f"UPDATE teams SET allowed='{json.dumps(allowed)}'")
        teamIds[getId(mess)] = teamId

        await bot.send_message(mess.chat.id, 'Ожидаем одобрения членов компании...', reply_markup=kb_leave)
        await findTeam(mess)

    elif mess.text == 'Поиск заново':
        if getId(mess) in rejAppl:
            rejAppl[getId(mess)].append(teams[getId(mess)])
        else:
            rejAppl[getId(mess)] = [teams[getId(mess)]]

        await find(mess)

    elif mess.text == 'Отклонить':
        rejects = json.loads(useSql(f"SELECT rejects FROM teams WHERE owner='{owners[getId(mess)]}'")[0][0])
        rejects.append(getId(mess))
        useSql(f"UPDATE teams SET rejects='{json.dumps(rejects)}' WHERE owner='{owners[getId(mess)]}'")

        await bot.send_message(mess.chat.id, 'Вы отклонили компанию', reply_markup=kb_menu)
        await reset(mess, getId(mess))

    elif mess.text == 'Одобрить компанию':
        for i in teams[getId(mess)]:
            invites = json.loads(useSql(f"SELECT invites FROM users WHERE username='{i}'")[0][0])
            invites.append(getId(mess))
            invites = json.dumps(invites)
            useSql(f"UPDATE users SET invites='{invites}' WHERE username='{i}'")

        teamId = random.randint(0, 1000)
        team = teams[getId(mess)]
        team.append(getId(mess))
        useSql(f"INSERT INTO teams (id, members, chat, allowed, owner, count, rejects) VALUES ({teamId}, '{json.dumps(team)}', '[]', '[]', '{getId(mess)}', {counts[getId(mess)]}, '[]')")
        teamIds[getId(mess)] = teamId
        owners[getId(mess)] = getId(mess)
        await bot.send_message(mess.chat.id, 'Ожидаем одобрения членов компании...', reply_markup=kb_leave)
        await findTeam(mess)

    else:
        if getId(mess) in action:
            if action[getId(mess)] == 'chat':
                teamId = teamIds[getId(mess)]
                team = useSql(f"SELECT * FROM teams WHERE id='{teamId}'")[0]
                username = getId(mess)
                chat = json.loads(team[2])
                chat.append([username, mess.text])
                chat = json.dumps(chat)
                useSql(f"UPDATE teams SET chat='{chat}' WHERE id={teamId}")

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
                    useSql(f"INSERT INTO users (username, name, photo, genre, anotherGenre, age, city, coordinates, invites, chatId) VALUES ('{getId(mess)}', '{name[getId(mess)]}', '{photo[getId(mess)]}', '{genre[getId(mess)]}', '{mess.text}', '{age[getId(mess)]}', '{city[getId(mess)]}', '{json.dumps(coordinates[getId(mess)])}', '[]', {message.chat.id})")
                else:
                    useSql(f"INSERT INTO users (username, name, photo, genre, anotherGenre, age, city, coordinates, invites, chatId) VALUES ('{getId(mess)}', '{name[getId(mess)]}', '{photo[getId(mess)]}', '{genre[getId(mess)]}', '{mess.text}', '{age[getId(mess)]}', '{city[getId(mess)]}', '[]', '[]', {message.chat.id})")

                await mess.reply('Анкета готова', reply_markup=kb_menu)
                if not(isEditing):
                    loop = asyncio.get_event_loop()
                    loop.create_task(findInvites(mess.chat.id, getId(mess)))



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
    # if not(useSql("SELECT * FROM users WHERE username='Mot05112'")):
    #     useSql("INSERT INTO users (username, name, photo, city, age, genre, anotherGenre, coordinates, invites) VALUES ('Mot05112', 'Пользователь7', 'AgACAgIAAxkBAANFZMD_2JbJdUG2Pfj5078xutZgDtsAAoTLMRtTywlKYfsUcoHV56IBAAMCAANtAAMvBA', 'Киров', 14, 'Мужской', 'Мужской', '[56.084518, 56.680753]', '[]')")
    # if not(useSql("SELECT * FROM users WHERE username='l1'")):
    #     useSql("INSERT INTO users (username, name, photo, city, age, genre, anotherGenre, coordinates, invites) VALUES ('l1', 'Пользоатель3', 'AgACAgIAAxkBAANFZMD_2JbJdUG2Pfj5078xutZgDtsAAoTLMRtTywlKYfsUcoHV56IBAAMCAANtAAMvBA', 'Киров', 14, 'Мужской', 'Женский', '[56.084518, 56.680753]', '[]')")
    # if not(useSql("SELECT * FROM users WHERE username='l2'")):
    #     useSql("INSERT INTO users (username, name, photo, city, age, genre, anotherGenre, coordinates, invites) VALUES ('l2', 'Пользоатель4', 'AgACAgIAAxkBAANFZMD_2JbJdUG2Pfj5078xutZgDtsAAoTLMRtTywlKYfsUcoHV56IBAAMCAANtAAMvBA', 'Киров', 14, 'Женский', 'Не важно', '[]', '[]')")
    # if not(useSql("SELECT * FROM users WHERE username='l3'")):
    #     useSql("INSERT INTO users (username, name, photo, city, age, genre, anotherGenre, coordinates, invites) VALUES ('l3', 'Пользоатель5', 'AgACAgIAAxkBAANFZMD_2JbJdUG2Pfj5078xutZgDtsAAoTLMRtTywlKYfsUcoHV56IBAAMCAANtAAMvBA', 'Киров', 14, 'Женский', 'Женский', '[]', '[]')")
    # if not(useSql("SELECT * FROM users WHERE username='l4'")):
    #     useSql("INSERT INTO users (username, name, photo, city, age, genre, anotherGenre, coordinates, invites) VALUES ('l4', 'Пользоатель6', 'AgACAgIAAxkBAANFZMD_2JbJdUG2Pfj5078xutZgDtsAAoTLMRtTywlKYfsUcoHV56IBAAMCAANtAAMvBA', 'Киров', 14, 'Женский', 'Мужской', '[56.084518, 56.680753]', '[]')")

    loop = asyncio.get_event_loop()
    users = useSql("SELECT username, chatId FROM users")
    for i in users:
        if i[1]:
            loop.create_task(findInvites(i[1], i[0]))

    executor.start_polling(dp, skip_updates=True)