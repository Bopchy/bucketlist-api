import json
from faker import Factory
from flask import Flask
from flask_testing import TestCase


class TestBucketlistUserEndpoints(TestCase):

    """Tests for class Bucketlist's User related endpoints"""

    def create_app(self):
        test_app = Flask(__name__)
        test_app.config['TESTING'] = True
        return test_app

    def setUp(self):
        fake_data = Factory.create()
        self.username = fake_data.user_name()
        self.password = fake_data.password()
        self.email = fake_data.email()

        # Creating a user
        new_user_url = '/auth/login'
        new_user_data = {'username': 'guty45', 'email': 'guty45@gmail.com', 'password': '1234abc'}
        self.client.post(new_user_url, data=json.dumps(new_user_data, sort_keys=True))

    def test_register_takes_username_email_and_password(self):
        url = '/auth/register'
        data = {'username': '', 'email': '', 'password': ''}
        response = self.client.post(url, data=json.dumps(data, sort_keys=True))
        self.assertEqual(response.status_code, 400)

    def test_register_returns_201_if_successful(self):
        url = '/auth/register'
        data = {'username': self.username, 'email': self.email, 'password': self.password}
        response = self.client.post(url, data=json.dumps(data, sort_keys=True))
        self.assertEqual(response.status_code, 201)

    def test_register_returns_400_if_username_blank(self):
        url = '/auth/register'
        data = {'username': '', 'email': self.email, 'password': self.password}
        response = self.client.post(url, data=json.dumps(data, sort_keys=True))
        self.assertEqual(response.status_code, 400)

    def test_register_returns_400_if_password_blank(self):
        url = 'auth/register'
        data = {'username': self.username, 'email': self.email, 'password': ''}
        response = self.client.post(url, data=json.dumps(data, sort_keys=True))
        self.assertEqual(response.status_code, 400)

    def test_register_returns_422_if_wrong_email_format(self):
        url = 'auth/register'
        data = {'username': self.username, 'email': 'ruthgmail.com', 'password': self.password}
        response = self.client.post(url, data=json.dumps(data, sort_keys=True))
        self.assertEqual(response.status_code, 422)

    def test_register_returns_400_if_email_blank(self):
        url = 'auth/register'
        data = {'username': self.username, 'email': '', 'password': self.password}
        response = self.client.post(url, data=json.dumps(data, sort_keys=True))
        self.assertEqual(response.status_code, 400)

    def test_register_returns_409_if_username_already_exists(self):
        url = 'auth/register'

        data1 = {'username': 'bopt67', 'email': self.email, 'password': self.password}
        response1 = self.client.post(url, data=json.dumps(data1, sort_keys=True))
        self.assertEqual(response1.status_code, 201)

        data2 = {'username': 'bopt67', 'email': 'bop67@gmail.com', 'password': self.password}
        response2 = self.client.post(url, data=json.dumps(data2, sort_keys=True))
        self.assertEqual(response2.status_code, 409)

    def test_register_returns_409_if_email_already_exists(self):
        url = 'auth/register'

        data1 = {'username': 'rety56', 'email': 'ret56@gmail.com', 'password': self.password}
        response1 = self.client.post(url, data=json.dumps(data1, sort_keys=True))
        self.assertEqual(response1.status_code, 201)

        data2 = {'username': self.password, 'email': 'ret56@gmail.com', 'password': self.password}
        response2 = self.client.post(url, data=json.dumps(data2, sort_keys=True))
        self.assertEqual(response2.status_code, 409)

    def test_login_returns_200_if_successful(self):
        url = '/auth/login'
        data = {'username': 'guty45', 'password': '1234abc'}
        response = self.client.post(url, data=json.dumps(data, sort_keys=True))
        self.assertEqual(response.status_code, 200)

    def test_login_returns_401_if_user_does_not_exist(self):
        url = '/auth/login'
        data = {'username': 'abcd12', 'password': '1234abc'}
        response = self.client.post(url, data=json.dumps(data, sort_keys=True))
        self.assertEqual(response.status_code, 401)
        self.assertIn('A user with that username does not exist.', response.data)

    def test_login_returns_401_if_wrong_password_used(self):
        url = '/auth/login'
        data = {'username': 'guty45', 'password': '5678def'}
        response = self.client.post(url, data=json.dumps(data, sort_keys=True))
        self.assertEqual(response.status_code, 401)

    def test_login_returns_400_if_no_credentials_provided(self):
        url = '/auth/login'
        data = {'username': '', 'password': ''}
        response = self.client.post(url, data=json.dumps(data, sort_keys=True))
        self.assertEqual(response.status_code, 400)

    def test_login_returns_400_if_no_password_provided(self):
        url = '/auth/login'
        data = {'username': 'guty45', 'password': ''}
        response = self.client.post(url, data=json.dumps(data, sort_keys=True))
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        pass
