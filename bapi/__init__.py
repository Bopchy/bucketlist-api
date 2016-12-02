from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt


app = Flask(__name__)

basic_auth = HTTPBasicAuth()

token_auth = HTTPTokenAuth()

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)
