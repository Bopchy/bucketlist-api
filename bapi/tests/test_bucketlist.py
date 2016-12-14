# import json
#
# from bapi.tests.test_setup import BaseTestClass
#
#
# class TestBucketListEndpoints(BaseTestClass):
#
#     """Tests class Bucketlist"""
#
#     def test_buckelist_is_created(self):
#         url = '/bucketlists/'
#         data = {'name': self.bucketlist_name}
#         # Get count before .post
#         response = self.client.post(url, data=json.dumps(data, sort_keys=True))
#         # Get count after post
#         # Assertion of +1 in count
#         self.assertEqual(response.status_code, 201)
#         self.assertIn("New Bucketlist '" + data['name'] + "' has been created.", response.data)
#
#     def test_create_bucketlist_returns_409_if_bucketlist_name_already_exists(self):
#         url = '/bucketlists/'
#         data = {'name': 'I need to do Y.'}
#         response = self.client.post(url, data=json.dumps(data, sort_keys=True))
#         self.assertEqual(response.status_code, 409)
#         self.assertIn('A bucketlist by this name already exists.', response.data)
#
#     def test_all_bucketlists_are_listed(self):
#         url = '/bucketlists/'
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#
#     def test_single_bucketlist_is_listed(self):
#         url = '/bucketlists/1'
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContain(response.message, 'Life Goals')
#
#     def test_bucketlist_is_updated(self):
#         url = '/bucketlists/1'
#         response = self.client.put(url)
#         self.assertEqual(response.status_code, 204)
#         self.assertIn('The bucketlist has been updated successfully.', response.data)
#
#     def test_bucketlist_is_deleted(self):
#         url = '/bucketlists/1'
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, 204)
#
#         url2 = '/bucketlists/1'
#         response2 = self.client.get(url2)
#         self.assertEqual(response2, 404)
#         self.assertIn("That bucketlist doesn't exist.", response2.data)
#
#     def test_new_item_created_in_bucketlist(self):
#         url = '/bucketlists/1/items/'
#         data = {'name': self.bucketlist_item_name}
#         response = self.client.post(url, data=json.dumps(data))
#         self.assertEqual(response.status_code, 201)
#
#     def test_existing_bucketlist_item_is_updated(self):
#         url = '/bucketlists/1/items/1'
#         data = {'name': 'Go bungee jumping on a waterfall.'}
#         response = self.client.put(url, data=json.dumps(data))
#         self.assertEqual(response.status_code, 204)
#
#     def test_updating_non_existing_bucketlist_item_returns_404(self):
#         url = '/bucketlists/1/items/2'
#         data = {'name': 'Go dancing on the moon.'}
#         response = self.client.put(url, data=json.dumps(data))
#         self.assertEqual(response.status_code, 404)
#
#     def test_bucketlist_item_is_deleted(self):
#         url = '/bucketlists/1/items/1'
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, 204)
#
#         url2 = '/bucketlists/1/items/1'
#         response2 = self.client.get(url2)
#         self.assertEqual(response2.status_code, 404)
#         self.assertIn("That bucketlist item doesn't exist.", response2.data)
