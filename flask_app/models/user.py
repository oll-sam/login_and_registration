import re
from flask_app import app
from flask import flash
from flask_app.config.mysqlconnection import MySQLConnection

class User:

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def insert_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUE (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return MySQLConnection("login_registration").query_db(query,data)

    @classmethod
    def get_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        db = MySQLConnection("login_registration").query_db(query,data)
        users= []

        for u in db:
            users.append(cls(u))

        return users



    @staticmethod
    def validate_user(data):
        valid = True

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

        if len(data["first_name"]) < 2 :
            valid = False
            flash("First name is required!")

        if len(data["last_name"]) < 2:
            valid = False
            flash("Last name is required!")

        if not EMAIL_REGEX.match(data["email"]):
            valid = False
            flash("Invalid Email")

        if len(User.get_email(data)) > 0:
            valid = False
            flash("Email is already in use!")

        if len(data["password"]) < 8:
            valid = False
            flash("Password is invalid!")

        if data["password"] != data["confirm_password"]:
            valid = False
            flash("Must confirm password!")

        return valid
