import json

from faker import Factory
from flask_testing import TestCase
# from flask_restful import Api

from bapi import app, db
from bapi.config import config
from bapi.bucketlist_models import Bucketlist, BucketListItem, Users
from bapi.index import api
# from bapi.resources.login import Login
# from bapi.resources.register import Register
# from bapi.resources.bucketlist_ops import Bucketlists, SingleBucketlist
# from bapi.resources.bucketlist_items import CreateBucketlistItem, BucketlistItems
# from bapi.routes import routes


class BaseTestClass(TestCase):

    """Sets up testing app, and fake data."""

    def create_app(self):
        app.config.from_object(config['testing'])
        # api = Api(app)
        # routes(api)
        return app

    def setUp(self):
        fake_data = Factory.create()
        self.bucketlist_name = fake_data.sentence()
        self.bucketlist_item_name = fake_data.sentence()
        self.username = fake_data.user_name()
        self.password = fake_data.password()
        self.email = fake_data.email()

        # api.add_resource(Login, '/auth/login', endpoint='testlogin')
        # api.add_resource(Register, '/auth/register', endpoint='testregister')
        # api.add_resource(Bucketlists, '/bucketlists/', endpoint='testbucketlists')
        # api.add_resource(SingleBucketlist, '/bucketlists/<id>',
        #                  endpoint='testsinglebucketlist')
        # api.add_resource(CreateBucketlistItem, '/bucketlists/<id>/items/',
        #                  endpoint='testcreatebucketlistitem')
        # api.add_resource(BucketlistItems, '/bucketlists/<id>/items/<item_id>',
        #                  endpoint='testbucketlistitems')

        # Create test database
        db.create_all()

        # Creating a bucketlist
        # self.new_bucketlist_url = '/bucketlists/'
        # self.new_bucketlist_data = {'name': 'Life Goals.'}
        # self.client.post(self.new_bucketlist_url, data=json.dumps(self.new_bucketlist_data)
        #
        # new_bucketlist = Bucketlist('Life Goals.',)
        # db.session.add(new_bucketlist)

        # # Creating bucketlist item
        # self.new_bucketlist_item_url = '/bucketlists/1/items/'
        # self.new_bucketlist_item_data = {'name': 'Go bungee jumping.'}
        # self.client.post(self.new_bucketlist_item_url, data=json.dumps(self.new_bucketlist_item_data))
        #
        # new_bucketlist_item = BucketListItem('Go bungee jumping.', 'No')
        # db.session.add(new_bucketlist_item)

        # Creating a user
        self.new_user_url = '/auth/login'
        self.new_user_data = {'username': 'guty45', 'email': 'guty45@gmail.com', 'password': '1234abc'}
        self.client.post(self.new_user_url, data=json.dumps(self.new_user_data))

        new_user = Users('guty45', 'guty45@gamil.com', '1234abc')
        db.session.add(new_user)

        # Commits all of the additions to db
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
