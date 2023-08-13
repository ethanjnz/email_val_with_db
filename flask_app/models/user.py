from flask_app.config.mysql_connection import connect_To_MySQL
import re
from flask import flash

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

DATABASE = "email_validation_schema"


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.email = data["email"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create(cls, form_data):
        query = """
                INSERT INTO users (email)
                VALUES (%(email)s)
                """
        result = connect_To_MySQL(DATABASE).query_db(query, form_data)
        return result

    @classmethod
    def get_all(cls):
        query = " SELECT * FROM users"

        results = connect_To_MySQL(DATABASE).query_db(query)
        users = []
        for row in results:
            users.append(User(row))
        return users

    @staticmethod
    def val_email(user):
        is_valid = True
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid Email Address")
            is_valid = False
        return is_valid

    @classmethod
    def check_for_email(cls, email):
        query = """
                SELECT * FROM users
                WHERE email = %(email)s
                """
        data = {"email": email}

        results = connect_To_MySQL(DATABASE).query_db(query, data)

        if len(results) < 1:
            return None

        else:
            return User(results[0])

    @classmethod
    def delete(cls, user_id):
        query = """
                DELETE FROM users
                WHERE id = %(user_id)s
                """

        data = {"user_id": user_id}
        connect_To_MySQL(DATABASE).query_db(query, data)
        return
