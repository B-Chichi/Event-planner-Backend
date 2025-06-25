from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin

# Global naming convention
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(metadata=metadata)


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text,nullable=False)
    email = db.Column(db.VARCHAR, unique=True)
    password = db.Column(db.VARCHAR)


    events = db.relationship("Event", back_populates="user")
    reviews = db.relationship("Review", back_populates="user")
    invitations = db.relationship("Invitation", back_populates="user")


    serialize_rules = ("-password", "-invitations","-events","-reviews")


class Category(db.Model, SerializerMixin):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    events = db.relationship("Event", back_populates="category")


class Event(db.Model, SerializerMixin):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    title = db.Column(db.Text)
    venue = db.Column(db.Text)
    date = db.Column(db.Text)
    description = db.Column(db.Text)
    image = db.Column(db.Text)

    reviews = db.relationship("Review", back_populates="event")
    invitations = db.relationship("Invitation", back_populates="event")
    user = db.relationship("User", back_populates="events")
    category = db.relationship("Category", back_populates="events")





class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now())

    user = db.relationship("User", back_populates="reviews")
    event = db.relationship("Event", back_populates="reviews")





class Invitation(db.Model, SerializerMixin):
    __tablename__ = "invitations"

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.now())

    user = db.relationship("User", back_populates="invitations")
    event = db.relationship("Event", back_populates="invitations")



