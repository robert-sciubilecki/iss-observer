import requests
import datetime as dt
import time

MY_LNG = 17.038538
MY_LAT = 51.107883


def check_for_iss():

    response_iss = requests.get(url='http://api.open-notify.org/iss-now.json')
    response_iss.raise_for_status()
    data = response_iss.json()['iss_position']
    iss_longitude, iss_latitude = float(data['longitude']), float(data['latitude'])

    config = {
        'lat': MY_LAT,
        'lng': MY_LNG,
        'formatted': 0
    }

    response_sunrise_sunset = requests.get(url='https://api.sunrise-sunset.org/json', params=config)
    response_sunrise_sunset.raise_for_status()
    data = response_sunrise_sunset.json()['results']
    sunrise = int(data['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['sunset'].split('T')[1].split(':')[0])
    now_hour = int(str(dt.datetime.now().time()).split(':')[0])
    overhead = round(MY_LNG) in range(round(iss_longitude) - 5, round(iss_longitude) + 5) \
        and round(MY_LAT) in range(round(iss_latitude) - 5, round(iss_latitude) + 5)

    night = now_hour not in range(sunrise, sunset)

    if overhead and night:
        print('iss overhead')
    else:
        print("There's nothing to be seen here")


while True:
    check_for_iss()
    time.sleep(60)
