import requests
import smtplib
from datetime import datetime
import time

MY_LAT = 36.852924
MY_LONG = -75.977982

MY_EMAIL = "my_email@yahoo.com"
MY_PASSWORD = "1234567"

SMTP_ADDRESS_BOOK = {"yahoo.com":"smtp.mail.yahoo.com", "gmail.com":"smtp.gmail.com", "hotmail.com":"smtp.live.com", "outlook.com":"smtp-mail.outlook.com"}

def is_iss_overhead():
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()

    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if iss_latitude <= MY_LAT + 5 and iss_latitude >= MY_LAT - 5 and iss_longitude <= MY_LONG + 5 and iss_longitude >= MY_LONG - 5:
        return True


def is_dark_out():
    parameters = {
        "lat":MY_LAT,
        "lgn":MY_LONG,
        "formatted":0
    }

    response = requests.get(url='https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int((data['results']['sunrise']).split('T')[1].split(':')[0])
    sunset = int((data['results']['sunset']).split('T')[1].split(':')[0])

    now = datetime.now()
    hour = now.hour

    if hour < sunrise or hour > sunset:
        return True

while True:
    if is_iss_overhead() == True and is_dark_out() == True:
        try:
            smtp_address = SMTP_ADDRESS_BOOK[MY_EMAIL.split('@')[-1].lower()]
        except KeyError as message:
            smtp_address = input(f"{message} is not a compatible server. Please input your server smtp: \n")
            if smtp_address == '':
                quit()

        with smtplib.SMTP(smtp_address) as connection:

            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)

            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg="Subject: Look Up! \n\n The international space station is above you.")
    time.sleep(60)









