import pyrebase
import os

config = {
    "apiKey": "AIzaSyD7w1t1naoWypN4eEZUhiZhq0l0G6xMdvk",
    "authDomain": "projectmanagement-3e8a8.firebaseapp.com",
    "databaseURL": "https://projectmanagement-3e8a8-default-rtdb.firebaseio.com",
    "projectId": "projectmanagement-3e8a8",
    "storageBucket": "projectmanagement-3e8a8.appspot.com",
    "messagingSenderId": "398063613086",
    "appId": "1:398063613086:web:05aa2a5bb0ccb2d821778f",
    "measurementId": "G-DBHEPCK3YT"
}

firebase = pyrebase.initialize_app(config=config)
authentication = firebase.auth()
database = firebase.database()
storage = firebase.storage()

email = "sunny@gmail.com"
password = "123456"

user = authentication.sign_in_with_email_and_password(email, password)
url = storage.child("/DESKTOP-3S7MM6C").get_url(user["idToken"])
print(url)