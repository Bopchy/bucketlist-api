import json

from flask import Flask
from faker import Factory
from flask_testing import TestCase

from api import app, db
from api.config import config
from api.bucketlist_models import Bucketlist, BucketListItem, Users


class BaseTestClass(TestCase):

    """Sets up testing app, and fake data."""

    def create_app(self):
        # test_app = Flask(__name__)
        # test_app.config.from_object(config['testing'])

        # db.init_app(test_app)
        # return test_app
        app.config.from_object(config['testing'])
        return app

    def setUp(self):
        fake_data = Factory.create()
        self.bucketlist_name = fake_data.sentence()
        self.bucketlist_item_name = fake_data.sentence()
        self.username = fake_data.user_name()
        self.password = fake_data.password()
        self.email = fake_data.email()

        # Create test database
        db.create_all()

        # Creating a bucketlist
        self.new_bucketlist_id = 1
        self.new_bucketlist_url = '/bucketlists/'
        self.new_bucketlist_data = {'name': 'Life Goals.'}
        self.client.post(self.new_bucketlist_url, data=json.dumps(self.new_bucketlist_data, sort_keys=True))

        new_bucketlist = Bucketlist('Life Goals.')
        db.session.add(new_bucketlist)

        # Creating bucketlist item
        self.new_bucketlist_item_id = 1
        self.new_bucketlist_item_url = '/bucketlists/1/items/'
        self.new_bucketlist_item_data = {'name': 'Go bungee jumping.'}
        self.client.post(self.new_bucketlist_item_url, data=json.dumps(self.new_bucketlist_item_data, sort_keys=True))

        new_bucketlist_item = BucketListItem('Go bungee jumping.')
        db.session.add(new_bucketlist_item)

        # Creating a user
        self.new_user_url = '/auth/login'
        self.new_user_data = {'username': 'guty45', 'email': 'guty45@gmail.com', 'password': '1234abc'}
        self.client.post(self.new_user_url, data=json.dumps(self.new_user_data, sort_keys=True))

        new_user = Users('guty45', 'guty45@gamil.com', '1234abc')
        db.session.add(new_user)

        # Commits all of the additions to db
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
