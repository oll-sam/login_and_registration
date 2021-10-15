from flask_app import app
from flask import render_template,request,redirect, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from flask import flash

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user/register", methods=['POST'])
def validate_user():
    # validate User
    # if user is valid, create record on DB
    # redirect to /success
    if User.validate_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": pw_hash,
            "id" : session["id"]
        }
        User.insert_user(data)
        flash("Great! Now you can login!")
        
    return redirect("/")


@app.route("/user/login", methods=['POST'])
def login():
    users = User.get_email(request.form)
    if len(users) != 1:
        flash("Email incorrect")
        return redirect ("/")

    user = users[0]

    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Password incorrect")
        return redirect('/')

    session["id"] = user.id
    session["first_name"]= user.first_name
    session["last_name"]= user.last_name
    session["email"] = user.email

    return redirect("/welcome")

@app.route("/welcome")
def welcome():
    if "id" not in session:
        flash("Please login")
        return redirect ("/")

    return render_template("welcome.html")

@app.route("/logout")
def logout():
    session.clear
    flash("You are now logged out. See Ya!")
    return redirect("/")