import requests
import os
from twilio.rest import Client

OWENDPOINT = 'https://api.openweathermap.org/data/3.0/onecall?'
OWAPIKEY = os.environ.get('OWAPIKEY_ENV')
LAT = 0
LON = 0
TWILIOSID = os.environ.get('TWILIOSID_ENV')
TWILIOTOKEN = os.environ.get('TWILIOTOKEN_ENV')
TELFROM = ''
TELTO = ''

def get_weather():

    query = {
        'lat' : LAT,
        'lon' : LON,
        'exclude' : 'current,minutely,daily',
        'appid' : OWAPIKEY
    }

    response = requests.get(OWENDPOINT, params=query)
    response.raise_for_status()
    data = response.json()
    data_hourly = data['hourly']
    data_hourly_12 = data_hourly[:12]
    is_umbrella_needed = [int(data['weather'][0]['id'])<700 for data in data_hourly_12]
    if True in is_umbrella_needed: send_sms()

def send_sms():
    account_sid = TWILIOSID
    auth_token = TWILIOTOKEN
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="It's going to rain today. Remember to bring an umbrella!",
                        from_=TELFROM,
                        to=TELTO
                    )

    print(message.status)
    
get_weather()