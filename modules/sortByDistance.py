from modules.getDistance import *
def sortByDistance(username, data):
    N = len(data)
    for i in range(N - 1):
        for j in range(N - i - 1):
            if getDistance(username, data[j][1])[0] > getDistance(username, data[j + 1][1])[0]:
                data[j], data[j + 1] = data[j + 1], data[j]

    return data