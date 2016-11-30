import itertools
from flask_restful import Resource, reqparse

from bucketlist_models import DB, Users, Bucketlist, BucketListItem
from serializers import *


class BapiUsers(Resource):

    def post(self):
        self.bapi_users = reqparse.RequestParser()
        self.bapi_users.add_argument('username', type=str, required=True, location='json')
        self.bapi_users.add_argument('email', type=str, required=True, location='json')
        self.bapi_users.add_argument('password', type=str, required=True, location='json')
        self.args = self.bapi_users.parse_args()
        
        for k, v in self.args.items():
            if k == self.args.username and v == None:
                return errors['UsernameRequiredError']
            elif k == self.args.email and v == None:
                return errors['EmailRequiredError']
            elif k == self.args.password and v == None:
                return errors['PasswordRequiredError']
            else:
                user = Users(username=self.args.username, email=self.args.email,
                    hashed_password=self.args.password)
        try:
            DB.session.add(user) 
            DB.session.commit()
            return {'message': self.args.username + ' has been successfully added.'}, 201 
        except Exception as e:
            DB.session.rollback()
            return {'message': e }

    def put(self):
        pass


class BapiRegister(Resource):
    """Registers new users."""

    def post():
        pass


class Bucketlists(Resource):

    """Create a new Bucketlist, List all Bucketlists."""

    def get():
        pass

    def post():
        pass


class SingleBucketlist(Resource):

    """List update and delete a single Bucketlist."""

    def get():
        pass

    def put():
        pass

    def delete():
        pass


class BucketlistItems(Resource):

    """Update and Delete BucketlistItems."""
        
    def put():
        pass

    def delete():
        pass


class CreateBucketlistItem(Resource): 
    """Create a new Item in Bucketlist."""

    def post():
    	pass

    	
