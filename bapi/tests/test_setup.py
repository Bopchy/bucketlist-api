import json

from faker import Factory
from flask_testing import TestCase
from flask import url_for
from bapi import app, db
from bapi.config import config
from bapi.bucketlist_models import Bucketlist, BucketListItem, Users
from bapi.index import api


class BaseTestClass(TestCase):

    """Sets up testing app, and fake data."""

    def create_app(self):
        app.config.from_object(config['testing'])
        return app

    def setUp(self):
        fake_data = Factory.create()
        self.bucketlist_name = fake_data.sentence()
        self.bucketlist_item_name = fake_data.sentence()
        self.username = fake_data.user_name()
        self.password = fake_data.password()
        self.email = fake_data.email()

        db.create_all()

        self.new_user_data = {'username': 'guty45',
                              'email': 'guty45@gmail.com',
                              'password': '1234abc'}
        self.client.post(url_for('register'),
                         data=json.dumps(self.new_user_data),
                         content_type='application/json')
        self.new_user = Users.query.filter_by(username='guty45').one()

        self.login_user_data = {'username': 'guty45', 'password': '1234abc'}
        response = self.client.post(url_for('bapilogin'),
                                    data=json.dumps(self.login_user_data),
                                    content_type='application/json')
        token = response.json['token']
        self.authorization = {'Authorization': 'Token {0}'.format(token)}

        self.new_bucketlist_data = {'name': 'Life Goals.',
                                    'created_by': self.new_user.id}
        self.client.post(url_for('bucketlists'),
                         data=json.dumps(self.new_bucketlist_data),
                         headers=self.authorization,
                         content_type='application/json')

        self.created_bucketlist = Bucketlist.query.filter_by(name=self.new_bucketlist_data['name']).one()
        self.new_bucketlist_item_data = {'name': 'Go bungee jumping.'}
        self.client.post(url_for('createbucketlistitem',
                         id=self.created_bucketlist.id),
                         data=json.dumps(self.new_bucketlist_item_data),
                         headers=self.authorization,
                         content_type='application/json')
        self.created_item = BucketListItem.query.filter_by(bucketlist_id=self.created_bucketlist.id).one()

        db.session.commit()
        db.session.expire_on_commit = False

    def tearDown(self):
        db.session.remove()
        db.drop_all()
