from flask_restful import Resource, reqparse
from models import Category, db
from flask import jsonify, request


class CategoryResource (Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", required= True, type=str, help="name is required")
    
    def get(self, id = None):
        if id is None:
            categories = Category.query.all()
            return jsonify([category.to_dict () for category in categories])

        else:
            category = Category.query.filter_by(id = id).first()
            if category is None : 
                return {"message": "category not found"}
            return jsonify(category.to_dict())


    def post(self):
        data = self.parser.parse_args()
        category = Category(**data)
        db.session.add(category)
        db.session.commit()

    def patch(self, id = None):
        data = self.parser.parse_args()
        category = Category.query.filter_by(id = id).first()
        category.name = data["name"]
        db.session.commit()
        return {"message"; "category updated successfully"}

     def delete(self, id = None):
        category =Category.query.filter_by(id = id).first()
        db.session.delete(category)
        db.session.commit()
        return {"message"; "category deleted successfully"}


            

            


