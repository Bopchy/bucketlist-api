from flask import request, url_for
from flask_restful import Api, Resource, reqparse, fields, marshal_with

from bapi import app, api


class Bapi(object):

    """class Bucketlist"""

    @app.route('', '/', '/auth/login', methods=['POST'])
    def user_login():
        pass

    @app.route('/auth/register', methods=['POST'])
    def register_user():
        pass

    @app.route('/bucketlists/', methods=['POST'])
    def create_bucketlist():
        pass

    @app.route('/bucketlists/', methods=['GET'])
    def list_bucketlists():
        pass

    @app.route('/bucketlists/<id>', methods=['GET'])
    def get_one_bucketlist():
        pass

    @app.route('/bucketlists/<id>', methods=['PUT'])
    def update_bucketlist():
        pass

    @app.route('/bucketlists/<id>', methods=['DELETE'])
    def delete_bucketlist():
        pass

    @app.route('/bucketlists/<id>/items/', methods=['POST'])
    def create_new_item_in_bucketlist():
        pass

    @app.route('/bucketlists/<id>/items/<item_id>', methods=['PUT'])
    def update_bucketlist_item():
        pass

    @app.route('/bucketlists/<id>/items/<item_id>', methods=['DELETE'])
    def delete_bucketlist_item():
        pass

bucketlist = {
    'id': fields.Integer
    'name': fields.String
    'items':
    'date_created': fields.
    'date_modified': fields.
    'created_by':
}

bucketlist_item = {
    'id': fields.Integer
    'name': fields.String
    'date_created':
    'date_modified':
    'done':
}

bapi_users = {
    'username': fields.String
    'email': fields.String
    'password':
}

class BapiUsers(Resource):

    """Bapi Users' resource - Logs users into bapi."""

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
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


# API resource routing setup 
api.add_resource(BapiUsers, '', '/', '/auth/login', endpoint='login')
api.add_resource(BapiRegister, '/auth/register', endpoint='register')
api.add_resource(Bucketlists, '/bucketlists/', endpoint='bucketlists')
api.add_resource(SingleBucketlist, '/bucketlists/<id>', endpoint='singlebucketlist')
api.add_resource(CreateBucketlistItem, '/bucketlists/<id>/items/', endpoint='createbucketlistitem')
api.add_resource(BucketlistItems, '/bucketlists/<id>/items/<item_id>', endpoint='bucketlistitems')


if (__name__) == '__main__':
    app.run(debug=True)
