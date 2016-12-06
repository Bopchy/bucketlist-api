import itertools
from datetime import datetime
from json import dumps 

from flask import g
from flask_restful import Resource, reqparse, marshal

from bucketlist_models import DB, Users, Bucketlist, BucketListItem
from serializers import bucketlist, bucketlist_item, bapi_users 
from verification import token_auth
from utils import json_serializer 


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

    """Creates a new Bucketlist and lists all Bucketlists.
    
    @token_auth.login_required ensures that users are required 
    to be authenticated and have a token."""

    @token_auth.login_required
    def get(self):
        # Lists all existing bucketlists
        all_bucketlists = Bucketlist.query.filter_by(created_by=g.user.id).all()
        if all_bucketlists:
            return marshal(all_bucketlists, bucketlist) 
        return {'message': 'There are currently no existing bucketlists.'}, 204
            
    
    @token_auth.login_required
    def post(self):
        # Creates a new bucketlist
        self.bucketlist = reqparse.RequestParser()
        self.bucketlist.add_argument('name', type=str, required=True, location='json')
        self.args = self.bucketlist.parse_args()

        if self.args.name == None:
            return {'message': 'You need to give your new bucketlist a name.'}, 400
        new_bucketlist = Bucketlist(name=self.args.name, created_by=g.user.id)

        try:
            DB.session.add(new_bucketlist)
            DB.session.commit()
            return {'message': 'New Bucketlist has been created successfully.'}, 201
        except Exception as e:
            DB.session.rollback()
            return {'message': e }, 500


class SingleBucketlist(Resource):

    """List, update and delete a single Bucketlist."""

    @token_auth.login_required
    def get(self, id):
        # Lists a single bucketlist 
        requested_bucketlist = Bucketlist.query.filter_by(created_by=g.user.id, id=id).first()
        if requested_bucketlist:
            return marshal(requested_bucketlist, bucketlist)
        return {'message': 'You do not have a bucketlist with that id.'}, 204

    @token_auth.login_required
    def put(self, id):
        # Updates a single bucketlist (entirely, not partly)
        self.new = reqparse.RequestParser()
        self.new.add_argument('name', type=str, required=True, location='json')
        self.args = self.new.parse_args()

        if self.args:
            bucketlist = Bucketlist.query.filter_by(created_by=g.user.id, id=id).first()
            old_name = bucketlist.name
            if bucketlist:
                try:
                    bucketlist.name = self.args.name
                    DB.session.commit()
                    return {'message': "'" + old_name + "'" + ' has been changed to ' + "'" + self.args.name + "'"}
                except Exception as e:
                    DB.session.rollback()
                    return {'message': e}
            return {'message': 'A bucketlist with that id does not exist'}, 404
        return {'message': 'You need to provide a new name to edit this Bucketlist.'}, 204

    @token_auth.login_required
    def delete(self, id):
        # Deletes a single bucketlist 
        if id:
            try:
                Bucketlist.query.filter_by(created_by=g.user.id, id=id).delete()
                DB.session.commit()
            except Exception as e:
                DB.session.rollback()
                return {'message': e}
        return 'You must provide a bucketlist id to delete a Bucketlist.', 204


class CreateBucketlistItem(Resource): 

    """Create a new Item in Bucketlist."""
    
    done_responses = ['yes', 'no']

    @token_auth.login_required
    def post(self, id):
        create_item = reqparse.RequestParser()
        create_item.add_argument('name', type=str, required=True, location='json')
        create_item.add_argument('done', type=str, required=False, default='No', location='json')
        create_item.add_argument('bucketlist_id', type=int, required=True, location='json')
        args = create_item.parse_args()

        if id:
            bucketlist = Bucketlist.query.filter_by(created_by=g.user.id, id=id).first()
            if bucketlist:
                if args.done == 'No':
                    done = False
                else:
                    done = True
                new_bucketlist_item = BucketListItem(name=args.name, done=done)
                new_bucketlist_item.bucketlist_id = bucketlist.id
                import ipdb; ipdb.set_trace()
                try:
                    DB.session.add(new_bucketlist_item)
                    DB.session.commit()
                    return {'message': " New item '" + args.name + "' has been created."}
                except Exception as e:
                    DB.session.rollback()
                    return {'message': e}
                    
            return {'message': 'A bucketlist with that id does not exist.'}, 400

        return {'message': 'You need to provide a bucketlist id for this operation.'}, 400


class BucketlistItems(Resource):

    """Update and Delete BucketlistItems."""
    
    @token_auth.login_required    
    def put():
        pass

    @token_auth.login_required
    def delete():
        pass

