import itertools

from flask import g
from flask_restful import Resource, reqparse

from bucketlist_models import DB, Users, Bucketlist, BucketListItem
from serializers import *
from verification import token_auth


class BapiLogin(Resource):

    """Logs in users and returns token."""

    def post(self):
        self.user = reqparse.RequestParser()
        self.user.add_argument('username', type=str, required=True, location='json')
        self.user.add_argument('password', type=str, required=True, location='json')
        self.args = self.user.parse_args()

        if self.args.username and self.args.password:
            user = Users.query.filter_by(username=self.args.username).first()
            if user:
                if user.check_password(self.args.password):
                    token = user.generate_auth_token()
                    return {'token': token}, 200
                return {'message': 'Invalid password'}, 401
            return {'message': args.username + ' does not exist in the database.'}, 401
        return {'message': 'Username or Password not provided.'}, 400


class BapiRegister(Resource):

    """Registers new users."""

    def post(self):
        self.bapi_users = reqparse.RequestParser()
        self.bapi_users.add_argument('username', type=str, required=True, location='json')
        self.bapi_users.add_argument('email', type=str, required=True, location='json')
        self.bapi_users.add_argument('password', type=str, required=True, location='json')
        self.args = self.bapi_users.parse_args()
        
        for k, v in self.args.items():
            if v == None:
                return {'message':'Username, Email and Password are required.'}, 400
            user = Users.query.filter_by(username=self.args.username).first()
            if user:
                return {'message': self.args.username + ' already exists. Please choose another username.'}, 409
            user_email = Users.query.filter_by(email=self.args.email).first()
            if user_email:
                return {'message': self.args.email + ' is already in use. Please provide a different email.'}, 409   
            user = Users(username=self.args.username, email=self.args.email, hashed_password=self.args.password)
        try:
            DB.session.add(user) 
            DB.session.commit()
            return {'message': self.args.username + ' has been successfully added.'}, 201 
        except Exception as e:
            DB.session.rollback()
            return {'message': e }, 500


class Bucketlists(Resource):

    """Create a new Bucketlist, List all Bucketlists.
    @token_auth.login_required ensures that users are required 
    to be authenticated and have a token."""

    @token_auth.login_required
    def get(self):
        pass
    
    @token_auth.login_required
    def post():
        pass


class SingleBucketlist(Resource):

    """List update and delete a single Bucketlist."""


    @token_auth.login_required
    def get():
        pass

    @token_auth.login_required
    def put():
        pass

    @token_auth.login_required
    def delete():
        pass


class BucketlistItems(Resource):

    """Update and Delete BucketlistItems."""
    
    @token_auth.login_required    
    def put():
        pass

    @token_auth.login_required
    def delete():
        pass


class CreateBucketlistItem(Resource): 

    """Create a new Item in Bucketlist."""
    
    @token_auth.login_required
    def post():
        pass

