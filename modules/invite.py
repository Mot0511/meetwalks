from modules.useSql import *
from main import sortByDistance
from itertools import groupby
def invite(inviter, age, count, genre1, genre2, city, coordinates=None):
    users = []
    countUsers = 3
    if coordinates:
        if genre2 == 'Не важно':
            data = useSql(f"SELECT * FROM users WHERE (age < ({age} + 2) AND age > ({age} - 2)) AND city='{city}' AND anotherGenre='Не важно' AND NOT username='{inviter}' AND NOT coordinates='[]' ORDER BY RANDOM() LIMIT {countUsers}")
            if data == []:
                data = useSql(f"SELECT * FROM users WHERE (age < ({age} + 2) AND age > ({age} - 2)) AND city='{city}' AND genre='{genre1}' AND genre=anotherGenre AND NOT username='{inviter}' AND NOT coordinates='[]' ORDER BY RANDOM() LIMIT {countUsers}")
        else:
            data = useSql(f"SELECT * FROM users WHERE (age < ({age} + 2) AND age > ({age} - 2)) AND city='{city}' AND genre='{genre2}' AND anotherGenre='{genre1}' AND NOT username='{inviter}' AND NOT coordinates='[]' ORDER BY RANDOM() LIMIT {countUsers}")
            if data == []:
                data = useSql(f"SELECT * FROM users WHERE (age < ({age} + 2) AND age > ({age} - 2)) AND city='{city}' AND genre='{genre2}' AND anotherGenre='Не важно' AND NOT username='{inviter}' AND NOT coordinates='[]' ORDER BY RANDOM() LIMIT {countUsers}")
    
        if not (data == []):
            data = sortByDistance(inviter, data)
            for i in data:
                users.append(i[1])
    
        users = [el for el, _ in groupby(users)]
    if len(users) < countUsers:
        remainder = countUsers - len(users)
        if genre2 == 'Не важно':
            data = useSql(f"SELECT * FROM users WHERE (age < ({age} + 2) AND age > ({age} - 2)) AND city='{city}' AND anotherGenre='Не важно' AND NOT username='{inviter}' AND coordinates='[]' ORDER BY RANDOM() LIMIT {countUsers}")
            if data == []:
                data = useSql(f"SELECT * FROM users WHERE (age < ({age} + 2) AND age > ({age} - 2)) AND city='{city}' AND genre='{genre1}' AND genre=anotherGenre AND NOT username='{inviter}' AND coordinates='[]' ORDER BY RANDOM() LIMIT {countUsers}")

        else:
            data = useSql(f"SELECT * FROM users WHERE (age < ({age} + 2) AND age > ({age} - 2)) AND city='{city}' AND genre='{genre2}' AND anotherGenre='{genre1}' AND NOT username='{inviter}' AND coordinates='[]' ORDER BY RANDOM() LIMIT {countUsers}")
            if data == []:
                data = useSql(f"SELECT * FROM users WHERE (age < ({age} + 2) AND age > ({age} - 2)) AND city='{city}' AND genre='{genre2}' AND anotherGenre='Не важно' AND NOT username='{inviter}' AND coordinates='[]' ORDER BY RANDOM() LIMIT {countUsers}")


        if not(data == []):
            for i in data:
                users.append(i[1])

    print(users)
    if users:
        for i in users:
            useSql(f"INSERT INTO invites (user1, user2, showed, allowed) VALUES ('{inviter}', '{i}', 0, 0)")