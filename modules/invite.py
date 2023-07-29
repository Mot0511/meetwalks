from modules.useSql import *
from main import sortByDistance
from itertools import groupby
def invite(inviter, age, count, genre1, genre2, city, coordinates=None):
    users = []
    countUsers = 3
    if coordinates:
        if genre2 == 'Не важно':
            data = useSql(f"SELECT * FROM inSearch WHERE (age < ({age} + 2) AND age > ({age} - 2)) AND city='{city}' AND anotherGenre='Не важно' AND NOT username='{inviter}' AND count={count} AND NOT coordinates='[]' LIMIT {count - 1};")
            if data == []:
                data = useSql(f"SELECT * FROM inSearch WHERE (age < ({age} + 2) AND age > ({age} - 2)) AND city='{city}' AND genre='{genre1}' AND genre=anotherGenre AND NOT username='{inviter}' AND count={count} AND NOT coordinates='[]' LIMIT {count - 1};")
        else:
            data = useSql(f"SELECT * FROM inSearch WHERE (age < ({age} + 2) AND age > ({age} - 2)) AND city='{city}' AND genre='{genre2}' AND anotherGenre='{genre1}' AND NOT username='{inviter}' AND count={count} AND NOT coordinates='[]' LIMIT {count - 1};")
            if data == []:
                data = useSql(f"SELECT * FROM inSearch WHERE (age < ({age} + 2) AND age > ({age} - 2)) AND city='{city}' AND genre='{genre2}' AND anotherGenre='Не важно' AND NOT username='{inviter}' AND count={count} AND NOT coordinates='[]' LIMIT {count - 1};")
    
        if not (data == []):
            data = sortByDistance(inSearchData[1], data)
            for i in data:
                users.append(i[1])
    
        users = [el for el, _ in groupby(users)]
        if len(users) < countUsers:
            remainder = countUsers - len(users)
            if genre2 == 'Не важно':
                data = useSql(f"SELECT * FROM inSearch WHERE (age < ({age} + 2) AND age > ({age} - 2)) AND city='{city}' AND anotherGenre='Не важно' AND NOT username='{inviter}' AND coordinates='[]' AND count={count} LIMIT {remainder};")
                if data == []:
                    data = useSql(f"SELECT * FROM inSearch WHERE (age < ({age} + 2) AND age > ({age} - 2)) AND city='{city}' AND genre='{genre1}' AND genre=anotherGenre AND NOT username='{inviter}' AND count={count} AND coordinates='[]' LIMIT {remainder};")

            else:
                data = useSql(f"SELECT * FROM inSearch WHERE (age < ({age} + 2) AND age > ({age} - 2)) AND city='{city}' AND genre='{genre2}' AND anotherGenre='{genre1}' AND NOT username='{inviter}' AND coordinates='[]' AND count={count} LIMIT {remainder};")
                if data == []:
                    data = useSql(f"SELECT * FROM inSearch WHERE (age < ({age} + 2) AND age > ({age} - 2)) AND city='{city}' AND genre='{genre2}' AND anotherGenre='Не важно' AND NOT username='{inviter}' AND count={count} AND coordinates='[]' LIMIT {remainder};")

    
            if not(data == []):
                for i in data:
                    users.append(i[1])

    if users:
        for i in users:
            useSql(f"INSERT INTO invites (user1, user2) VALUES ({inviter}, {i})")