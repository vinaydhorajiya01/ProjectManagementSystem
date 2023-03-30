import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

app = Flask(__name__)
config = {
    "apiKey": "AIzaSyDXoDR0eixnIXtaO--ve9IYNzwoQ7mu6wg",
    "authDomain": "project-management-syste-89346.firebaseapp.com",
    "databaseURL": "https://project-management-syste-89346-default-rtdb.firebaseio.com",
    "projectId": "project-management-syste-89346",
    "storageBucket": "project-management-syste-89346.appspot.com",
    "messagingSenderId": "139850838241",
    "appId": "1:139850838241:web:20fecdcb0197938a2407a0",
    "measurementId": "G-W8HK76YNWM"
}

firebase = pyrebase.initialize_app(config=config)
auth = firebase.auth()
database = firebase.database()

person = {
    "is_logged_in": False,
    "name": "",
    "email": "",
    "uid": ""
}


# Login
@app.route("/")
def login():
    return render_template("login.html")


@app.route("/welcome")
def welcome():
    if person['is_logged_in'] == True:
        return render_template("welcome.html", email=person['email'], name=person['name'])
    else:
        return redirect(url_for("login"))


@app.route("/result", methods=["post", "get"])
def result():
    if request.method == "POST":
        result = request.form
        email = result['email']
        password = result['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)

            # Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user['email']
            person['uid'] = user['localId']

            # Get the name of the user
            data = database.child("users").get()
            person['name'] = data.val()[person["uid"]["name"]]
            return redirect(url_for("welcome"))
        except:
            return redirect(url_for("login"))
    else:
        if person['is_logged_in'] == True:
            return redirect(url_for("welcome"))
        else:
            return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
