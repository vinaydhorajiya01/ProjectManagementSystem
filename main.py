import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)
app.secret_key = "session"
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
auth = firebase.auth()
database = firebase.database()


# Login
@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            auth.sign_in_with_email_and_password(email, password)
            session["user_email"] = email
            return redirect(url_for("welcome"))
        except:
            return "failed to login"
    return render_template("login.html")


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


@app.route("/forget-password", methods=["POST", "GET"])
def forget_password():
    if request.method == "POST":
        cred = credentials.Certificate('firebase_private_key.json')
        firebase_admin.initialize_app(cred)
        email = request.form.get("email")
        user = firebase_admin.auth.get_user_by_email(email)
        if user.uid == None:
            pass
        else:
            redirect(url_for('reset_password'))
    return render_template("forget_password.html")


@app.route("/reset-password")
def reset_password():
    return render_template("set_password.html")




if __name__ == "__main__":
    app.run(debug=True)