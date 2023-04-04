import os.path

import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory
import firebase_admin
from werkzeug.utils import secure_filename
from firebase_admin import credentials, auth

app = Flask(__name__)
app.secret_key = "session"
# app.config['UPLOAD'] = "static/uploads/"

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
cred = credentials.Certificate('firebase_private_key.json')


# Login
@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            user = authentication.sign_in_with_email_and_password(email, password)
            if user is not None:
                cred = credentials.Certificate('firebase_private_key.json')
                firebase_admin.initialize_app(cred)
                user_id = firebase_admin.auth.get_user_by_email(email)
                session['user_id'] = user_id.uid
                session["user_email"] = email
                admin_user = database.child("Admin").get()
                admin_user_email = admin_user.val()
                session['user_name'] = admin_user_email['Sunny']['fname']

                if email == admin_user_email['Sunny']['email']:
                    return redirect(url_for("admin", name=session.get('user_name')))
                else:
                    return redirect(url_for('welcome'))
            else:
                flash("Please check your credentials!!!")
        except Exception as e:
            flash(e)
    return render_template("login.html")


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


@app.route("/admin")
def admin():
    employees = database.child("Employee").get()
    total_employee = len(employees.val())
    admin_user = database.child("Admin").get().val()
    return render_template("admin.html", name=admin_user['Sunny']['fname'], total_employee=total_employee)


@app.route("/admin/details")
def details():
    admin_user = database.child("Admin").get().val()
    fname = admin_user['Sunny']['fname']
    mname = admin_user['Sunny']['mname']
    lname = admin_user['Sunny']['lname']
    position = admin_user['Sunny']['position']
    email = admin_user['Sunny']['email']
    gender = admin_user['Sunny']['gender']
    phone = admin_user['Sunny']['phone']
    dob = admin_user['Sunny']['dob']
    quote = admin_user['Sunny']['quote']
    return render_template("details.html", fname=fname, mname=mname, lname=lname, position=position, email=email,
                           gender=gender, phone=phone, dob=dob, quote=quote)


@app.route("/admin/employee", methods=['get', 'post'])
def employee():
    if request.method == 'POST' and request.form.get('editForm'):
        name = request.form.get("name")
        position = request.form.get("position")
        id = request.form.get("id")
        phone = request.form.get("phone")
        email = request.form.get("email")
        department = request.form.get("department")
        doj = request.form.get("doj")
        result = database.child("Employee").get()
        for res in result.each():
            if id == res.val()['id']:
                key = res.key()
        database.child("Employee").child(key).update({
            "name": name,
            "position": position,
            "phone": phone,
            "email": email,
            "department": department,
            "doj": doj
        })
        flash("Data update successfully.")
    employee = database.child('Employee').get()
    return render_template('employee.html', employee=employee)


@app.route("/admin/employee/add", methods=["POST", "GET"])
def addEmployee():
    if request.method == "POST":
        name = request.form.get("name")
        position = request.form.get("position")
        id = request.form.get("id")
        phone = request.form.get("phone")
        email = request.form.get("email")
        department = request.form.get("department")
        doj = request.form.get("doj")
        file = request.files["profile_pic"]
        profile_pic = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD'], profile_pic))
        storage.child("employee_images").put(profile_pic)
        data = {
            "name": name,
            "position": position,
            "id": id,
            "phone": phone,
            "email": email,
            "department": department,
            "doj": doj
        }
        database.child("Employee").push(data)
        redirect(url_for("employee"))
    return redirect(url_for("employee"))


@app.route("/admin/employee/remove/<id>")
def removeData(id):
    data = database.child("Employee").get()
    for record in data.each():
        if record.val()['id'] == id:
            database.child("Employee").child(record.key()).remove()
            flash("Data deleted successfully.")
            return redirect(url_for("employee"))
    return None


@app.route("/admin/settings", methods=['get', 'post'])
def setting():
    if request.method == "POST":
        current_password = request.form.get("currentpassword")
        password = request.form.get("password")
        repeat_password = request.form.get("repeatpassword")
        if current_password == repeat_password:
            flash("Please enter different password.")
        elif password == repeat_password:
            firebase_admin.initialize_app(cred)
            firebase_admin.auth.update_user(uid=session.get('user_id'), password=password)
            flash("Password updated successfully")
    return render_template("settings.html")


@app.route("/forget-password", methods=["POST", "GET"])
def forget_password():
    if request.method == "POST":
        cred = credentials.Certificate('firebase_private_key.json')
        firebase_admin.initialize_app(cred, name="forget")
        email = request.form.get("email")
        user = firebase_admin.auth.get_user_by_email(email)
        if user.uid is not None:
            session['user_id'] = user.uid
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


@app.route("/")
def logout():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
