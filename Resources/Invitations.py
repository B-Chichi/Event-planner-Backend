from flask import jsonify
from flask_restful import Resource, reqparse
from datetime import datetime
from flask_mail import Message

from models import Invitation, db, User, Event
from app import mail  


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

        # Fetch related user and event details
        user = db.session.get(User, data["user_id"])
        event = db.session.get(Event, data["event_id"])

        if user and event:
            try:
                subject = f"You're invited to {event.title}!"
                body = f"""
                Hi {user.name},

                You've been invited to attend "{event.title}" on {event.date} at {event.venue}.

                Description: {event.description}

                We hope to see you there!
                """

                msg = Message(subject, recipients=[user.email])
                msg.body = body
                mail.send(msg)
            except Exception as e:
                return {
                    "message": "Invitation saved but email failed",
                    "error": str(e),
                }, 500

        return {"message": "invitation sent successfully"}

    def patch(self, id):
        data = self.parser.parse_args()
        invitation = db.session.get(Invitation, id)
        if invitation is None:
            return {"message": "invitation not found"}, 404

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
            return {"message": "invitation not found"}, 404
        db.session.delete(invitation)
        db.session.commit()
        return {"message": "invitation deleted"}
