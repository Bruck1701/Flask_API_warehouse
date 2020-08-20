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
            item.save_to_db()
        except:
            return {"message": "Error has occurred inserting the item"}, 500

        return item.json(), 201

  
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'message': 'Item deleted'}

        

    
    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
     
        if item is None:
            item = ItemModel(None,name,data['price'])
        else:
            item.price = data['price']
        item.save_to_db()

        return item.json()
            


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        results = cursor.execute(query).fetchall()
        connection.close()

        result_as_dict = []
        for result in results:
            result_as_dict.append({'name': result[1], 'price': result[2]})

        return {"items": result_as_dict}, 200
