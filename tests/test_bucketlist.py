import json
from faker import Factory
from flask import Flask
from flask_testing import TestCase


class TestBucketListEndpoints(TestCase):

    """Tests class Bucketlist"""

    def create_app(self):
        testing_app = Flask(__name__)
        testing_app.config['TESTING'] = True
        return testing_app

    def setUp(self):
        fake_data = Factory.create()
        self.bucketlist_name = fake_data.sentence()

        # Creating a bucketlist
        new_bucketlist_url = '/bucketlists/'
        new_bucketlist_data = {'name': 'Life Goals.'}
        self.client.post(new_bucketlist_url, data=json.dumps(new_bucketlist_data, sort_keys=True))

    def test_buckelist_is_created(self):
        url = '/bucketlists/'
        data = {'name': self.bucketlist_name}
        response = self.client.post(url, data=json.dumps(data, sort_keys=True))
        self.assertEqual(response.status_code, 201)
        self.assertIn("New Bucketlist '" + ['name'] + "' has been created.", response.data)

    def test_create_bucketlist_returns_409_if_bucketlist_name_already_exists(self):
        url = '/bucketlists/'
        data = {'name': 'I need to do Y.'}
        response = self.client.post(url, data=json.dumps(data, sort_keys=True))
        self.assertEqual(response.status_code, 409)
        self.assertIn('A bucketlist by this name already exists.', response.data)

    def test_all_bucketlists_are_listed(self):
        url = '/bucketlists/'
        reposnse = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_one_bucketlist_is_listed(self):
        url =

    def test_bucketlist_is_updated(self):
        pass

    def test_bucketlist_is_deleted(self):
        pass

    def test_new_item_created_in_bucketlist(self):
        pass

    def test_bucketlist_item_is_updated(self):
        pass

    def test_bucketlist_item_is_deleted(self):
        pass

    def test_public_access_is_false(self):
        pass

    def test_you_can_search_bucketlist_by_name(self):
        pass

    def tearDown(self):
        pass
