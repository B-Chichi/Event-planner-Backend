from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
#from datetime import timedelta


from models import db
from Resources.User import UserResource, LoginResource, SigninResource
from Resources.Events import EventResource
from Resources.Reviews import ReviewResource
from Resources.categories import CategoryResource
from Resources.Invitations import InvitationResource
from dotenv import load_dotenv
import os


# entry point of our flask application
app = Flask(__name__)
CORS(app, origins=["*"])

# setting up flask_restful
api = Api(app)
jwt = JWTManager(app)
load_dotenv()


# configuring our app
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
#app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False


# inorder to see our sql statements being logged out;
app.config["SQLALCHEMY_ECHO"] = True

migrate = Migrate(app, db)

db.init_app(app)


@app.get("/")
def index():
    return {"message": "Welcome to event planner"}


api.add_resource(UserResource, "/users", "/users/<int:id>")
api.add_resource(SigninResource, "/signin")
api.add_resource(LoginResource, "/login")
api.add_resource(EventResource, "/events","/events/<int:id>")
api.add_resource(ReviewResource, "/events/<int:event_id>/reviews")
api.add_resource(CategoryResource,"/categories","/categories/<int:id>")
api.add_resource(InvitationResource, "/invitations", "/invitations/<int:id>")
