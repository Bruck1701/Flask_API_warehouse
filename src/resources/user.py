import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="Cannot be blank"

                        )
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="Cannot be blank"
                        )

    def post(self):  # create a new user.

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return ({"message": "User already exists on the database"}), 400

        user = UserModel(**data)
        user.save_to_db()

        return ({"message": "User {} created succesfully".format(data["username"])}), 201
