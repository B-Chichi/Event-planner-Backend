from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Event, db


class EventResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("title", required=True, help="Title is required")
    parser.add_argument("venue", required=True, help="Venue is required")
    parser.add_argument("date", required=True, help="Date is required")
    parser.add_argument("description", required=True, help="Description is required")
    parser.add_argument("image", required=True, help="Image is required")
    parser.add_argument(
        "category_id", type=int, required=True, help="Category is required"
    )

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        events = Event.query.filter_by(user_id=user_id).all()
        return [event.to_dict() for event in events]

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = self.parser.parse_args()

        try:
            event = Event(user_id=int(user_id), **data)
            db.session.add(event)
            db.session.commit()
            return {
                "message": "Event created successfully",
                "event": event.to_dict(),
            }, 201
        except Exception as e:
            db.session.rollback()
            print("[ERROR] Event creation failed:", e)
            return {"message": "Internal Server Error"}, 500

    def delete(self, id):
        event = Event.query.filter_by(id=id).first()
        if event is None:
            return {"message": "Event not found"}, 404

        db.session.delete(event)
        db.session.commit()
        return {"message": "Event deleted successfully"}
