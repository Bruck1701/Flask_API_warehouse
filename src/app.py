from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from datetime import timedelta
from resources.item import Item, ItemList
from resources.user import UserRegister

from db import db
import config

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.secret_key = config.SK
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

api = Api(app)
jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")


if __name__ == "__main__":
    db.init_app(app)

    app.run(port=5000, debug=True)
