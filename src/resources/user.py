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

        request_data = UserRegister.parser.parse_args()

        if UserModel.retrieve_by_username(request_data["username"]):
            return ({"message": "User already exists on the database"}), 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        insert_query = "INSERT INTO users VALUES (NULL,?,?)"
        cursor.execute(
            insert_query, (request_data["username"], request_data["password"]))

        connection.commit()
        connection.close()

        return ({"message": "User {} created succesfully".format(request_data["username"])}), 201
