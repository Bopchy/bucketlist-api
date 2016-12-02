import base64

from flask import request, g
from flask_httpauth import HTTPBasicAuth
from flask_login import login_required
from flask_restful import Api

from bapi import app, auth
from config import config
from bucketlist_models import Users, Bucketlist, BucketListItem
from routes import routes

api = Api(app)
app.config.from_object(config['development'])
routes(api)

if (__name__) == '__main__':
    app.run(debug=True)
