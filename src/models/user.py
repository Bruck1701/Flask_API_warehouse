
import sqlite3
from db import db



class UserModel(db.Model):

    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def retrieve_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        select_query = "SELECT * from users WHERE username=? "
        result = cursor.execute(select_query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def retrieve_by_id(cls, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        select_query = "SELECT * from users WHERE id=? "
        result = cursor.execute(select_query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user
