from flask_restful import Resource, reqparse
from sqlalchemy import func
from models import Category, db
from sqlalchemy.exc import SQLAlchemyError


class CategoryResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", required=True, type=str, help="Category name is required"
    )

    def get(self, id=None):
        if id is None:
            categories = Category.query.all()
            return [cat.to_dict() for cat in categories], 200

        category = Category.query.filter_by(id=id).first()
        if not category:
            return {"message": "Category not found"}, 404
        return category.to_dict(), 200

    def post(self):
        try:
            data = self.parser.parse_args()
            name = data["name"].strip()

            if not name:
                return {"message": "Category name cannot be empty"}, 400

            # Case-insensitive duplicate check
            existing = Category.query.filter(
                func.lower(Category.name) == name.lower()
            ).first()
            if existing:
                return {"id": existing.id, "name": existing.name}, 200

            new_category = Category(name=name)
            db.session.add(new_category)
            db.session.commit()

            return {"id": new_category.id, "name": new_category.name}, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": f"Database error: {str(e)}"}, 500
        except Exception as e:
            return {"message": f"Server error: {str(e)}"}, 500

    def patch(self, id=None):
        category = Category.query.filter_by(id=id).first()
        if not category:
            return {"message": "Category not found"}, 404

        data = self.parser.parse_args()
        category.name = data["name"].strip()
        db.session.commit()
        return {"message": "Category updated successfully"}

    def delete(self, id=None):
        category = Category.query.filter_by(id=id).first()
        if not category:
            return {"message": "Category not found"}, 404

        db.session.delete(category)
        db.session.commit()
        return {"message": "Category deleted successfully"}
