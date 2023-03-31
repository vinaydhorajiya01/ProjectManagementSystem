import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, url_for
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
authentication = firebase.auth()
database = firebase.database()
cred = credentials.Certificate('firebase_private_key.json')
firebase_admin.initialize_app(cred)


# Login
@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            authentication.sign_in_with_email_and_password(email, password)
            session["user_email"] = email
            return redirect(url_for("welcome"))
        except:
            flash("Please check your crendentials!!!")
    return render_template("login.html")


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


@app.route("/forget-password", methods=["POST", "GET"])
def forget_password():
    if request.method == "POST":
        cred = credentials.Certificate('firebase_private_key.json')
        firebase_admin.initialize_app(cred, name="forget")
        email = request.form.get("email")
        user = firebase_admin.auth.get_user_by_email(email)
        if user.uid is not None:
            return redirect(url_for("reset_password", user_id=user.uid))
        else:
            flash("User does not exist!!!")
    return render_template("forget_password.html")


@app.route("/reset-password/<user_id>", methods=["post", "get"])
def reset_password(user_id):
    if request.method == "POST":
        if request.form.get("password") == request.form.get("cpassword"):
            password = request.form.get("password")
            firebase_admin.auth.update_user(uid=user_id, password=password)
            return render_template("login.html")
        elif request.form.get("password") is None and request.form.get("cpassword") is None:
            flash("Enter the some value in fields.")
        else:
            flash("Both value should be same.")
    return render_template("reset_password.html", user_id=user_id)


if __name__ == "__main__":
    app.run(debug=True)
