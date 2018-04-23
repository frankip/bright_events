"""
This files test for failed login scenarios
"""
from __future__ import absolute_import

import json
import unittest
from config import app_config
from app import app, db


class FailedUserAuthTestCase(unittest.TestCase):
    """Test cases that result in failed login or registration"""

    def setUp(self):
        """Set up test variables."""
        self.app = app
        self.app.config.from_object(app_config['testing'])
        self.client = self.app.test_client
        self.user_data = {
            'first_name': 'new',
            'last_name': 'user',
            'email': 'test@example.com',
            'password': 'Test_password1'
        }
        # Binds app to current context
        with self.app.app_context():
            #create all tables
            db.create_all()
            
    def test_invalid_registration(self):
        """Test registration will fail if not all inputs are present"""
        missing_name = {
            'last_name': 'user',
            'email': 'test@example.com',
            'password': 'test_password'
        }
        resp = self.client().post('/api/auth/register/', data=missing_name)
        result = json.loads(resp.data.decode())['message']
        self.assertIn(
            result, 'ensure the first name field is not empty and it consist of alphabets only')

    def test_failed_login(self):
        """Test non registered users cannot login."""
        not_a_user = {
            'email': 'not_a_user@example.com',
            'password': 'nope'
        }
        res = self.client().post('/api/auth/login/', data=not_a_user)
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data.decode())['message']
        self.assertIn(result, "Invalid Email or Password, Please Try again")

    def test_invalid_password(self):
        """test to ensure password requires more than six characters and both upper and lower case"""
        user1 = {
            'first_name': 'new',
            'last_name': 'user',
            'email': 'test@example.com',
            'password': '1234'
        }
        user2 = {
            'first_name': 'new',
            'last_name': 'user',
            'email': 'test@example.com',
            'password': '12345Ab'
        }
        # Test for user with password less than six characters
        resp = self.client().post('/api/auth/register/', data=user1)
        self.assertEqual(resp.status_code, 400)
        result = json.loads(resp.data.decode())['message']
        # self.assertIn(
        #     result, 'Password field can not be empty and it should contain an Uppercase, a lowercase, a digit and shoud be more than six characters')

        # Test for user with more than six characters
        resp2 = self.client().post('/api/auth/register/', data=user2)
        self.assertEqual(resp2.status_code, 201)
        result = json.loads(resp2.data.decode())['message']
        self.assertIn(result, 'user has been created')

    def test_missing_password_field(self):
        """Test that registration will fail when the password field is missing"""
        user1 = {
            'first_name': 'new',
            'last_name': 'user',
            'email': 'test@example.com',
        }
        resp = self.client().post('/api/auth/register/', data=user1)
        self.assertEqual(resp.status_code, 400)
        result = json.loads(resp.data.decode())['message']
        self.assertIn(
            result, 'Password field can not be empty and it should contain an Uppercase, a lowercase, a digit and shoud be more than six characters')




    def test_duplicate_emails(self):
        """Test that a user cannot be registered twice."""
        self.client().post('/api/auth/register/', data=self.user_data)
        resp_2 = self.client().post('/api/auth/register/', data=self.user_data)
        self.assertEqual(resp_2.status_code, 202)
        result = json.loads(resp_2.data.decode())['message']
        self.assertIn(result, 'User already exists. Please login.')

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
