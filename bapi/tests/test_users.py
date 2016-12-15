import json


from bapi.tests.test_setup import BaseTestClass


class TestBucketlistUserEndpoints(BaseTestClass):

    """Tests for class Bucketlist's User related endpoints"""

    def test_register_returns_201_if_successful(self):
        url = 'http://localhost:5000/auth/register'
        data = {'username': self.username,
                'email': self.email, 'password': self.password}
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual('New user has been added successfully.',
                         response.json['message'])

    def test_register_returns_422_if_wrong_email_format(self):
        url = 'http://localhost:5000/auth/register'
        data = {'username': 'guty45', 'email': 'ruthgmail.com',
                'password': '1234abc'}
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 422)
        self.assertEqual('Invalid email provided', response.json['message'])

    def test_register_returns_409_if_username_already_exists(self):
        url = 'http://localhost:5000/auth/register'

        data = {'username': 'guty45', 'email': self.email,
                'password': self.password}
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 409)
        self.assertEqual('A user with that name already exists.',
                         response.json['message'])

    def test_register_returns_409_if_email_already_exists(self):
        url = 'http://localhost:5000/auth/register'
        data = {'username': self.username, 'email': 'guty45@gmail.com',
                'password': self.password}
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 409)
        self.assertEqual('That email is already in use.',
                         response.json['message'])

    def test_login_returns_200_if_successful(self):
        url = 'http://localhost:5000/auth/login'
        data = {'username': 'guty45', 'password': '1234abc'}
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)

    def test_login_returns_401_if_user_does_not_exist(self):
        url = 'http://localhost:5000/auth/login'
        data = {'username': 'abcd12', 'password': self.password}
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual('That username does not exist.',
                         response.json['message'])

    def test_login_returns_401_if_wrong_password_used(self):
        url = 'http://localhost:5000/auth/login'
        data = {'username': 'guty45', 'password': '5678def'}
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_login_returns_400_if_no_password_provided(self):
        url = 'http://localhost:5000/auth/login'
        data = {'username': 'guty45', 'password': ''}
        response = self.client.post(url, data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
