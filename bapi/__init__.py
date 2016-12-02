from flask import Flask
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt


app = Flask(__name__)

token_auth = HTTPTokenAuth(scheme='Token')

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)
