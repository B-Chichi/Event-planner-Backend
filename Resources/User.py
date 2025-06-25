from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from flask_bcrypt import generate_password_hash, check_password_hash

from models import User, db

class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, help="Name is required")
    parser.add_argument("email", required=True, help="Email is required")
    parser.add_argument("password", required=True, help="Password is required")
    
    def get(self, id=None):
        if id is None:
            users = User.query.all()
            return [user.to_dict() for user in users]

        else:
            user = User.query.filter_by(id=id).first()

            if user is None:
                return {"message": "User not found"}, 404
            
            return user.to_dict()
        
    def patch(self, id):
        data = self.parser.parse_args()

        user = User.query.filter_by(id=id).first()

        if user is None:
            return {"message": "User not found"}, 404

        user.name = data["name"]
        user.email = data["email"]
        user.password = data["password"]

        db.session.commit()

        return {"message": "User updated successfully"}
    
    def delete(self, id):
        user = User.query.filter_by(id=id).first()

        if user is None:
            return {"message": "User not found"}, 404
        
        db.session.delete(user)
        db.session.commit()

        return {"message": "User deleted successfully"}
   
class SigninResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, help="Name is required")
    parser.add_argument("email", required=True, help="Email is required")
    parser.add_argument("password", required=True, help="Password is required")

    def post(self):
        data = self.parser.parse_args()

        email = User.query.filter_by(email=data["email"]).first()

        if email:
            return{"message": "User already exists"}, 422
        
        hash = generate_password_hash(data["password"]).decode("utf-8")
        
        user = User(**data, password=hash)

        db.session.add(user)
        db.session.commit()

        return{"message": "User created successfully"}, 201
    
class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", required=True, type=str, help="Email address is required"
    )
    parser.add_argument(
        "password", required=True, type=str, help="Password is required"
    )

    def post(self):
        data = self.parser.parse_args()

        user = User.query.filter_by(email=data["email"]).first()

        if user is None:
            return {"message": "User does not exist"}, 401
        
        if check_password_hash(user.password, data["password"]):
            # access_token = create_access_token(identity=user.id)

            return {
                "message": "Login successful",
                "user": user.to_dict(),
                "access_token": "access_token"
            }, 201
        else:
            return {"message": "Invalid email or password"}, 401

