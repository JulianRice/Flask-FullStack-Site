from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object(Config)      #Load configuration file we made at config.py

db = MongoEngine()
db.init_app(app)

from application import routes

