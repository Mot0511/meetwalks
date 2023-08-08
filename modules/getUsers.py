from modules.sortByDistance import *
from useSql import *
from itertools import groupby

def getUsers(user, count, rejAppl=None):
    strRej = ''
    if rejAppl:
        rejects = []
        for i in rejAppl:
            for j in i:
                if not(i in rejects):
                    rejects.append(j)

        for i in rejects:
            strRej += "AND NOT username='"+i+"' "

    users = []
    userdata = useSql(f"SELECT * FROM users WHERE username='{user}'")[0]
    if not (userdata[8] == '[]'):
        if userdata[5] == 'Не важно':
            print(1)
            data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND (anotherGenre='Не важно' OR (genre='{userdata[4]}' AND genre=anotherGenre)) AND NOT username='{userdata[1]}' AND NOT coordinates='[]' {strRej}ORDER BY RANDOM()")
        else:
            print(2)
            data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND ((genre='{userdata[5]}' AND anotherGenre='{userdata[4]}') OR (genre='{userdata[5]}' AND anotherGenre='Не важно')) AND NOT username='{userdata[1]}' AND NOT coordinates='[]' {strRej}ORDER BY RANDOM()")

        if not(data == []):
            data = sortByDistance(user, data)

            if len(data) < count - 1:
                for i in data:
                    users.append(i[1])
            else:
                for i in range(count - 1):
                    users.append(data[i][1])

            if len(users) == count - 1:
                return users

            else:
                if userdata[5] == 'Не важно':
                    print(3)
                    data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[4]}' AND genre=anotherGenre AND NOT username='{userdata[1]}' AND NOT coordinates='[]' {strRej}ORDER BY RANDOM()")
                else:
                    print(4)
                    data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND anotherGenre='Не важно' AND NOT username='{userdata[1]}' AND NOT coordinates='[]' {strRej}ORDER BY RANDOM()")
                data = sortByDistance(user, data)
                remainder = count - 1 - len(users)
                if len(data) < remainder:
                    for i in data:
                        users.append(i[1])
                else:
                    for i in range(remainder):
                        users.append(data[i][1])


                if len(users) == count - 1:
                    return users

    remainder = count - 1 - len(users)
    if userdata[5] == 'Не важно':
        data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND (anotherGenre='Не важно' OR (genre='{userdata[4]}' AND genre=anotherGenre)) AND NOT username='{userdata[1]}' AND coordinates='[]' {strRej}ORDER BY RANDOM()")

    else:
        data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND ((genre='{userdata[5]}' AND anotherGenre='{userdata[4]}') OR (genre='{userdata[5]}' AND anotherGenre='Не важно')) AND NOT username='{userdata[1]}' AND coordinates='[]' {strRej}ORDER BY RANDOM()")

    if not (data == []):
        if len(data) < remainder:
            for i in data:
                users.append(i[1])
        else:
            for i in range(remainder):
                users.append(data[i][1])


    if len(users) == count - 1:
        return users

    else:
        remainder = count - len(users)
        if userdata[5] == 'Не важно':
            data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[4]}' AND genre=anotherGenre AND NOT username='{userdata[1]}' AND coordinates='[]' {strRej}ORDER BY RANDOM()")
        else:
            data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND anotherGenre='Не важно' AND NOT username='{userdata[1]}' AND coordinates='[]' {strRej}ORDER BY RANDOM()")

        if len(data) < remainder:
            for i in data:
                users.append(i[1])
        else:
            for i in range(remainder):
                users.append(data[i][1])

        if len(users) == count - 1:
            return users


    users = [el for el, _ in groupby(users)]
    return users