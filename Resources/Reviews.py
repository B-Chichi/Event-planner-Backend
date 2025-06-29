from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Review, db
from datetime import datetime


class ReviewResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("rating", type=str, required=False, help="rating is required")
    parser.add_argument("comment", type=str, required=True, help="rating is required")
    parser.add_argument("created_at", type=str)

    @jwt_required()
    def get(self, event_id):
        reviews = Review.query.filter_by(event_id=event_id).all()
        return jsonify([r.to_dict() for r in reviews])

    @jwt_required()
    def post(self, event_id):
        user_id = get_jwt_identity()
        data = self.parser.parse_args()

        if not data["created_at"]:
            data["created_at"] = datetime.now()
        else:
            data["created_at"] = datetime.fromisoformat(data["created_at"])

        review = Review(
            user_id=int(user_id),
            event_id=event_id,
            rating=data["rating"],
            comment=data["comment"],
            created_at=data["created_at"],
        )
        db.session.add(review)
        db.session.commit()
        return {"message": "review submitted", "review": review.to_dict()}, 201
