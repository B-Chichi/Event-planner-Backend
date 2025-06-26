from flask_restful import Resource, reqparse
from flask import jsonify
from models import Invitation, db
from datetime import datetime


class InvitationResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "event_id", type=int, required=True, help="event_id is required"
    )
    parser.add_argument("user_id", type=int, required=True, help="user_id is required")
    parser.add_argument("status", type=str)
    parser.add_argument("created_at", type=str)

    def get(self, id=None):
        if id is None:
            invitations = Invitation.query.all()
            return jsonify([inv.to_dict() for inv in invitations])
        invitation = db.session.get(Invitation, id)
        if invitation is None:
            return {"message": "invitation not found"}, 404
        return jsonify(invitation.to_dict())

    def post(self):
        data = self.parser.parse_args()
        created_at = (
            datetime.fromisoformat(data["created_at"])
            if data["created_at"]
            else datetime.now()
        )

        invitation = Invitation(
            event_id=data["event_id"],
            user_id=data["user_id"],
            status=data["status"],
            created_at=created_at,
        )
        db.session.add(invitation)
        db.session.commit()
        return {"message": "invitation sent"}, 

    def patch(self, id):
        data = self.parser.parse_args()
        invitation = db.session.get(Invitation, id)
        if invitation is None:
            return {"message": "invitation not found"}, 

        if data["event_id"] is not None:
            invitation.event_id = data["event_id"]
        if data["user_id"] is not None:
            invitation.user_id = data["user_id"]
        if data["status"] is not None:
            invitation.status = data["status"]
        if data["created_at"] is not None:
            invitation.created_at = datetime.fromisoformat(data["created_at"])

        db.session.commit()
        return {"message": "invitation updated"}

    def delete(self, id):
        invitation = db.session.get(Invitation, id)
        if invitation is None:
            return {"message": "invitation not found"}, 
        db.session.delete(invitation)
        db.session.commit()
        return {"message": "invitation deleted"}