from pynput import keyboard, mouse
import time
from PIL import ImageGrab
import random
import time
import pyrebase
import platform
from datetime import datetime

t = 0
firebaseConfig = {
    "apiKey": "AIzaSyD7w1t1naoWypN4eEZUhiZhq0l0G6xMdvk",
    "authDomain": "projectmanagement-3e8a8.firebaseapp.com",
    "databaseURL": "https://projectmanagement-3e8a8-default-rtdb.firebaseio.com",
    "projectId": "projectmanagement-3e8a8",
    "storageBucket": "projectmanagement-3e8a8.appspot.com",
    "messagingSenderId": "398063613086",
    "appId": "1:398063613086:web:05aa2a5bb0ccb2d821778f",
    "measurementId": "G-DBHEPCK3YT"
}


def take_screenshot():
    snapshot = ImageGrab.grab()
    file_name = str(time.time())
    file_name = file_name.strip() + ".png"
    system_name = platform.uname().node
    snapshot.save(file_name)
    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()
    storage.child(system_name + "/" + file_name).put(file_name)

activity_times = [
  
]

while t != 15:
    now = datetime.now()
    current_time = now.strftime("%y-%m-%d %H:%M:%S")   

    with keyboard.Events() as events:
        event = events.get(1.0)

    with mouse.Events() as events1:
        event1 = events1.get(1.0)

    if event is None and event1 is None and t == 5 :
        activity_times.append({'inactive': current_time})

    elif event is not None or event1 is not None:
        activity_times.append({'active': current_time})

    elif t == random.randint(1, 10):
        take_screenshot()
    t+=1
    print(t)
    
# total_active_time = datetime.time(0, 0, 0)  # Initialize total active time to zero


# for activity in activity_times:
#     active_time = activity['active']
#     inactive_time = activity['inactive']
#     duration = inactive_time - active_time
#     total_active_time += duration  # Add the duration to the total active time

print(f"Total active time: { activity_times}")