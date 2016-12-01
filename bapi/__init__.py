from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt


app = Flask(__name__)

bcrypt=Bcrypt(app)

db = SQLAlchemy(app)

