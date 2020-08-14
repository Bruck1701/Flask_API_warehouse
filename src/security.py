from werkzeug.security import safe_str_cmp
from models.user import UserModel
import sqlite3


def authenticate(username, password):
    """Returns a user 
    if the the username exists in the db, and the passwords match.
    Parameters
    ----------
    username: str
    password: str
    """
    user = UserModel.retrieve_by_username(username)

    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return UserModel.retrieve_by_id(user_id)
