from flask_restful import Resource, reqparse

from models import Event, db


class EventResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("title", required=True, help="Title is required")
    parser.add_argument("venue", required=True, help="venue is required")
    parser.add_argument("date", required=True, help="date is required")
    parser.add_argument("user_id", type=int, required=True, help="User ID is required")
    parser.add_argument("category_id", type=int, required=True, help="Category ID is required")
    parser.add_argument("description", required=True, help="description is required")
    parser.add_argument("image", required=True, help="image is required")

    def get(self):
        events = Event.query.all()
        return [event.to_dict() for event in events]

    def post(self):
        data = self.parser.parse_args()

        event = Event(**data)

        db.session.add(event)
        db.session.commit()

        return {"message": "Event created successfully"}, 201

    def delete(self, id):
        event = Event.query.filter_by(id=id).first()

        if event is None:
            return {"message": "Event not found"}, 404

        db.session.delete(event)

        db.session.commit()

        return {"message": "Event deleted successfully"}
