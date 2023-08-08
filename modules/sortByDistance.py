from modules.getDistance import *
def sortByDistance(username, data):
    print(data)
    N = len(data)
    for i in range(N - 1):
        for j in range(N - i - 1):
            distance1 = getDistance(username, data[j][1])
            distance2 = getDistance(username, data[j + 1][1])
            if distance1[1] == 'км':
                distance1 = distance1[0] * 1000
            else:
                distance1 = distance1[0]

            if distance2[1] == 'км':
                distance2 = distance2[0] * 1000
            else:
                distance2 = distance2[0]

            if distance1 > distance2:
                data[j], data[j + 1] = data[j + 1], data[j]


    return data