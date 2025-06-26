from flask_restful import Resource, reqparse
from flask import jsonify
from models import Review, db
from datetime import datetime


class ReviewResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("rating", type=int, required=True, help="rating is required")
    parser.add_argument("comment", type=str)
    parser.add_argument("created_at", type=str) 

    def get(self, id=None):
        if id is None:
            reviews = Review.query.all()
            return jsonify([r.to_dict() for r in reviews])
        review = db.session.get(Review,id)
        if review is None:
            return {"message": "review not found"}, 404
        return jsonify(review.to_dict())

    def post(self):
        data = self.parser.parse_args()
        if not data["created_at"]:
            data["created_at"] = datetime.now()
        else:
            data["created_at"] = datetime.fromisoformat(data["created_at"])

        review = Review(
            rating=data["rating"],
            comment=data["comment"],
            created_at=data["created_at"],
        )
        db.session.add(review)
        db.session.commit()
        return {"message": "review submitted"},

    def patch(self, id):
        data = self.parser.parse_args()
        review = db.session.get(Review,id)
        if review is None:
            return {"message": "review not found"}, 404

        for field in ["rating", "comment", "created_at"]:
            if data[field] is not None:
                if field == "created_at":
                    setattr(review, field, datetime.fromisoformat(data[field]))
                else:
                    setattr(review, field, data[field])

        db.session.commit()
        return {"message": "review updated"}

    def delete(self, id):
        review = db.session.get(Review,id)
        if review is None:
            return {"message": "review not found"}, 
        db.session.delete(review)
        db.session.commit()
        return {"message": "review deleted"}
