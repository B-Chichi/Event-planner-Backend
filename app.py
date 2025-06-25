
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api

from models import db

#entry point of our flask application
app = Flask(__name__)

#setting up flask_restful
api = Api(app)

CORS(app)

#configuring our app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


#inorder to see our sql statements being logged out; 
app.config["SQLALCHEMY_ECHO"] = True

migrate = Migrate(app, db)

db.init_app(app)

