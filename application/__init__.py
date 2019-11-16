from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_restplus import Api

api = Api()
app = Flask(__name__)
app.config.from_object(Config)      #Load configuration file we made at config.py

db = MongoEngine()
db.init_app(app)
api.init_app(app) #Initiate API for Postman 

from application import routes

