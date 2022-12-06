import requests
import time
from datetime import datetime
from d_config import send_mail

MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude

def find_ISS(): 
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    #Your position is within +5 or -5 degrees of the ISS position.
    if iss_latitude < MY_LAT+5 and iss_latitude > MY_LAT-5 and iss_longitude < MY_LONG+5 and iss_longitude > MY_LONG-5:
        return True
    else:
        print("za daleko")

def check_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now_hour = datetime.now().hour
    
    if time_now_hour < sunrise or time_now_hour > sunset:
        print("noc")
        return True

#If the ISS is close to my current position
# and it is currently dark
while True:
    # BONUS: run the code every 60 seconds.
    if find_ISS() and check_night():
        # Then send me an email to tell me to look up.
        send_mail()
    time.sleep(60)