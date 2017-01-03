import json

from flask import url_for

from bapi.tests.test_setup import BaseTestClass


class TestBucketListEndpoints(BaseTestClass):

    """Tests class Bucketlist"""

    def test_buckelist_is_created(self):
        url = url_for('bucketlists')
        data = {'name': 'Other Goals.'}
        response = self.client.post(url, data=json.dumps(data),
                                    headers=self.authorization,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('New Bucketlist created successfully.',
                      response.json['message'])

    def test_create_bucketlist_returns_409_if_bucketlist_name_exists(self):
        url = url_for('bucketlists')
        data = {'name': 'Life Goals.'}
        response = self.client.post(url, data=json.dumps(data),
                                    headers=self.authorization,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 409)
        self.assertIn('You already have a Bucketlist with that name.',
                      response.json['message'])

    def test_all_bucketlists_are_listed(self):
        url = url_for('bucketlists')
        response = self.client.get(url, headers=self.authorization,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_single_bucketlist_is_listed(self):
        url = url_for('singlebucketlist', id=self.created_bucketlist.id)
        response = self.client.get(url, headers=self.authorization,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Life Goals.', response.json['name'])

    def test_bucketlist_is_updated(self):
        url = url_for('singlebucketlist', id=self.created_bucketlist.id)
        data = {'name': 'Life Goals 2017.'}
        response = self.client.put(url, data=json.dumps(data),
                                   headers=self.authorization,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Bucketlist edited successfully.',
                         response.json['message'])

    def test_bucketlist_is_deleted(self):
        url = url_for('singlebucketlist', id=self.created_bucketlist.id)
        response = self.client.delete(url, headers=self.authorization,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Bucketlist deleted successfully.',
                         response.json['message'])

    def test_new_item_created_in_bucketlist(self):
        url = url_for('createbucketlistitem', id=self.created_bucketlist.id)
        data = {'name': 'New test item.'}
        response = self.client.post(url, data=json.dumps(data),
                                    headers=self.authorization,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual('New item has been created.',
                         response.json['message'])

    def test_existing_bucketlist_item_is_updated(self):
        url = url_for('bucketlistitems', id=self.created_bucketlist.id,
                      item_id=self.created_item.id)
        data = {'name': 'Go bungee jumping on a waterfall.'}
        response = self.client.put(url, data=json.dumps(data),
                                   headers=self.authorization,
                                   content_type='application/json')
        self.assertEqual('Changes have been made succesfully.',
                         response.json['message'])
        self.assertEqual(response.status_code, 200)

    def test_updating_non_existing_bucketlist_item_returns_404(self):
        url = url_for('bucketlistitems', id=self.created_bucketlist.id,
                      item_id=8)
        data = {'name': 'Go dancing on the moon.'}
        response = self.client.put(url, data=json.dumps(data),
                                   headers=self.authorization,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual('An item with that id was not found.',
                         response.json['message'])

    def test_bucketlist_item_is_deleted(self):
        url = url_for('bucketlistitems', id=self.created_bucketlist.id,
                      item_id=self.created_item.id)
        response = self.client.delete(url, headers=self.authorization,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Item has been deleted successfully.',
                         response.json['message'])
