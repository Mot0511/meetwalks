from modules.sortByDistance import *
from useSql import *
from itertools import groupby

def getUsers(user, count):
    users = []
    userdata = useSql(f"SELECT * FROM users WHERE username='{user}'")[0]

    if not (userdata[8] == '[]'):
        if userdata[5] == 'Не важно':
            data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND anotherGenre='Не важно' AND NOT username='{userdata[1]}' AND NOT coordinates='[]'")
            if data == []:
                data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[4]}' AND genre=anotherGenre AND NOT username='{userdata[1]}' AND NOT coordinates='[]'")
        else:
            data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND anotherGenre='{userdata[4]}' AND NOT username='{userdata[1]}' AND NOT coordinates='[]'")
            if data == []:
                data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND anotherGenre='Не важно' AND NOT username='{userdata[1]}' AND NOT coordinates='[]'")

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
                    data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[4]}' AND genre=anotherGenre AND NOT username='{userdata[1]}' AND NOT coordinates='[]'")
                else:
                    data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND anotherGenre='Не важно' AND NOT username='{userdata[1]}' AND NOT coordinates='[]'")
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
        data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND anotherGenre='Не важно' AND NOT username='{userdata[1]}' AND coordinates='[]'")
        if data == []:
            data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[4]}' AND genre=anotherGenre AND NOT username='{userdata[1]}' AND coordinates='[]'")

    else:
        data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND anotherGenre='{userdata[4]}' AND NOT username='{userdata[1]}' AND coordinates='[]'")
        if data == []:
            data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND anotherGenre='Не важно' AND NOT username='{userdata[1]}' AND coordinates='[]'")

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
            data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[4]}' AND genre=anotherGenre AND NOT username='{userdata[1]}' AND coordinates='[]' LIMIT {remainder - 1};")
        else:
            data = useSql(f"SELECT * FROM users WHERE (age < ({userdata[6]} + 2) AND age > ({userdata[6]} - 2)) AND city='{userdata[7]}' AND genre='{userdata[5]}' AND anotherGenre='Не важно' AND NOT username='{userdata[1]}' AND coordinates='[]' LIMIT {remainder - 1};")

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