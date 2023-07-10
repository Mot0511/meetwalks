from modules.useSql import *
from datetime import datetime

def getStatistics():
    month = datetime.now().month
    year = datetime.now().year
    day = datetime.now().day

    monthSearches = 0
    monthTeams = 0
    monthUsers = 0
    monthData = useSql(f"SELECT * FROM statistics WHERE month={month} AND year={year}")
    for i in monthData:
        monthSearches += i[4]
        monthTeams += i[5]
        monthUsers += i[6]

    dayData = useSql(f"SELECT * FROM statistics WHERE day={day} AND month={month} AND year={year}")
    if dayData:
        daySearches = dayData[0][4]
        dayTeams = dayData[0][5]
        dayUsers = dayData[0][6]
    else:
        daySearches = 0
        dayTeams = 0
        dayUsers = 0

    searches = 0
    teams = 0
    users = 0
    data = useSql(f"SELECT * FROM statistics")
    for i in data:
        searches += i[4]
        teams += i[5]
        users += i[6]

    res = f'Новых поисков за этот день: {daySearches}\n' \
          f'Новых команд за этот день: {dayTeams}\n' \
          f'Новых пользователей за этот день: {dayUsers}\n\n' \
          f'Новых поисков за этот месяц: {monthSearches}\n' \
          f'Новых команд за этот месяц: {monthTeams}\n' \
          f'Новых пользователей за этот месяц: {monthUsers}\n\n' \
          f'Всего поисков: {searches}\n' \
          f'Всего формирований команд: {teams}\n' \
          f'Всего пользователей: {useSql("SELECT COUNT(*) FROM users")[0][0]}'

    return res

def new(obj):
    day = datetime.now().day
    month = datetime.now().month
    year = datetime.now().year

    data = useSql(f"SELECT * FROM statistics WHERE day={day} AND month={month} AND year={year}")

    if data:
        data = data[0]
        useSql(f"DELETE FROM statistics WHERE id={data[0]}")
        if obj == 'search':
            useSql(f"INSERT INTO statistics (id, day, month, year, searches, teams, users) VALUES ({data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4] + 1}, {data[5]}, {data[6]})")
        elif obj == 'teams':
            useSql(f"INSERT INTO statistics (id, day, month, year, searches, teams, users) VALUES ({data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5] + 1}, {data[6]})")
        elif obj == 'users':
            useSql(f"INSERT INTO statistics (id, day, month, year, searches, teams, users) VALUES ({data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}, {data[5]}, {data[6] + 1})")

    else:
        if obj == 'search':
            useSql(f"INSERT INTO statistics (day, month, year, searches, teams, users) VALUES ({day}, {month}, {year}, {1}, {0}, {0})")
        elif obj == 'teams':
            useSql(f"INSERT INTO statistics (day, month, year, searches, teams, users) VALUES ({day}, {month}, {year}, {0}, {1}, {0})")
        elif obj == 'users':
            useSql(f"INSERT INTO statistics (day, month, year, searches, teams, users) VALUES ({day}, {month}, {year}, {0}, {0}, {1})")