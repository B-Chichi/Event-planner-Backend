from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Event, Category, db


class EventResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("title", required=True, help="Title is required")
    parser.add_argument("venue", required=True, help="venue is required")
    parser.add_argument("date", required=True, help="date is required")
    parser.add_argument("user_id", type=int, required=True, help="User ID is required")
    parser.add_argument(
        "category_id", type=int, required=True, help="Category ID is required"
    )
    parser.add_argument("description", required=True, help="description is required")
    parser.add_argument("image", required=True, help="image is required")

    @jwt_required()
    def get(self):
        events = Event.query.all()
        return [event.to_dict() for event in events]

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()

        user_id = get_jwt_identity()
        data["user_id"] = user_id

        data["category_id"] = data.get("category_id") or 1

        category = Category.query.get(data["category_id"])
        if not category:
            return {"error": "Invalid category ID."}, 400

        event = Event(**data)

        db.session.add(event)
        db.session.commit()

        return {"message": "Event created successfully", "event": event.to_dict()}, 201

    @jwt_required()
    def delete(self, id):
        event = Event.query.filter_by(id=id).first()

        if event is None:
            return {"message": "Event not found"}, 404

        db.session.delete(event)

        db.session.commit()

        return {"message": "Event deleted successfully"}
