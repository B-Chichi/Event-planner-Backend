from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api

from models import db
from Resources.User import UserResource, LoginResource, SigninResource
from Resources.Events import EventResource
from Resources.Reviews import ReviewResource
from Resources.categories import CategoryResource

# entry point of our flask application
app = Flask(__name__)

# setting up flask_restful
api = Api(app)

CORS(app)

# configuring our app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


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
api.add_resource(EventResource, "/events", "/events/<int:id>")
api.add_resource(ReviewResource,"/reviews","/reviews/<int:id>")
api.add_resource(CategoryResource,"/categories","/categories/<int:id>")
