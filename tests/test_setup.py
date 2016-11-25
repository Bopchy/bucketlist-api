import json
from faker import Factory
from flask import Flask
from flask_testing import TestCase


class TestSetUpTearDown(TestCase):

    """Sets up testing app, and fake data."""

    def create_app(self):
        test_app = Flask(__name__)
        test_app.config['TESTING'] = True
        return test_app

    def setUp(self):
        fake_data = Factory.create()
        self.bucketlist_name = fake_data.sentence()
        self.bucketlist_item_name = fake_data.sentence()
        self.username = fake_data.user_name()
        self.password = fake_data.password()
        self.email = fake_data.email()

        # Creating a bucketlist
        new_bucketlist_id = 1
        new_bucketlist_url = '/bucketlists/'
        new_bucketlist_data = {'name': 'Life Goals.'}
        self.client.post(new_bucketlist_url, data=json.dumps(new_bucketlist_data, sort_keys=True))

        # Creating bucketlist item
        new_bucketlist_item_id = 1
        new_bucketlist_item_url = '/bucketlists/1/items/'
        new_bucketlist_item_data = {'name': 'Go bungee jumping.'}
        self.client.post(new_bucketlist_item_url, data=json.dumps(new_bucketlist_item_data, sort_keys=True))

        # Creating a user
        new_user_url = '/auth/login'
        new_user_data = {'username': 'guty45', 'email': 'guty45@gmail.com', 'password': '1234abc'}
        self.client.post(new_user_url, data=json.dumps(new_user_data, sort_keys=True))

    def tearDown(self):
        pass
