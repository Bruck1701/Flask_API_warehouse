import sqlite3
import json
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="Cannot be blank"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()

        return ({"message": "Item not found"}), 404

   

    def post(self, name):

        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"])

        if ItemModel.find_by_name(name):
            return ({"message": "Error: Item already exists"})

        try:
            item.insert()
        except:
            return {"message": "Error has occurred inserting the item"}, 500

        return item.json(), 201

  
    def delete(self, name):

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {"message": "Item deleted"}

    
    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name,data["price"])

        if item:
            try:
                updated_item.update()
            except:
                return ({"message": "An error has occurred updating the item price"}), 500
        else:
            try:
                updated_item.insert()
            except:
                return({"message": "An error has occurred creating the new item"}), 500
        return updated_item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        results = cursor.execute(query).fetchall()
        connection.close()

        result_as_dict = []
        for result in results:
            result_as_dict.append({'name': result[0], 'price': result[1]})

        return {"items": result_as_dict}, 200
