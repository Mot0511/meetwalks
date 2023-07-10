import json
from geopy.distance import geodesic
from modules.useSql import useSql

def getDistance(user, applicant):
    userCoordinates = json.loads(useSql(f"SELECT coordinates FROM users WHERE username='{user}'")[0][0])
    applicantCoordinates = json.loads(useSql(f"SELECT coordinates FROM users WHERE username='{applicant}'")[0][0])
    if userCoordinates and applicantCoordinates:
        distance = geodesic(userCoordinates, applicantCoordinates).km
        unit = 'км'
        if int(distance) == 0:
            distance *= 1000
            unit = 'м'

        return [int(distance), unit]

    return None