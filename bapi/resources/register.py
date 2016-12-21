from flask_restful import Resource, reqparse
import re

from bapi import db
from bapi.bucketlist_models import Users


class Register(Resource):

    """Registers new users."""

    def post(self):
        self.bapi_users = reqparse.RequestParser()
        self.bapi_users.add_argument('username', type=str, required=True,
                                     location='json')
        self.bapi_users.add_argument('email', type=str, required=True,
                                     location='json')
        self.bapi_users.add_argument('password', type=str, required=True,
                                     location='json')
        self.args = self.bapi_users.parse_args()

        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                        self.args.email):
            return {'message': 'Invalid email provided'}, 422
        user = Users.query.filter_by(username=self.args.username).first()
        if user:
            return {'message': 'A user with that name already exists.'}, 409
        user_email = Users.query.filter_by(email=self.args.email).first()
        if user_email:
            return {'message': 'That email is already in use.'}, 409
        user = Users(username=self.args.username, email=self.args.email,
                     hashed_password=self.args.password)

        try:
            db.session.add(user)
            db.session.commit()
            return {'message': 'New user has been added successfully.'}, 201
        except Exception:
            db.session.rollback()
            return {'message': 'An error occured during saving.'}, 500
