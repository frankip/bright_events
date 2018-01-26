"""
This files test the Authentication endpoints functionality
"""
from __future__ import absolute_import

import unittest
import json
from config import app_config
from app import app, db


class UserAuthTestcase(unittest.TestCase):
    """Test case for the authentication functionality."""

    def setUp(self):
        """Set up test variables."""
        self.app = app
        self.app.config.from_object(app_config['testing'])
        self.client = self.app.test_client
        self.user_data = {
            'first_name': 'new',
            'last_name': 'user',
            'email': 'test@example.com',
            'password': 'test_password'
            }
        
        with self.app.app_context():
            #create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

        # Binds app to current context
        with self.app.app_context():
            #create all tables
            db.create_all()

    def test_user_registration(self):
        """Test user registration works correcty."""
        resp = self.client().post('/api/auth/register/', data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        self.assertIn("user has been created", str(resp.data))

    def test_user_login(self):
        """Test registered user can login."""
        resp = self.client().post('/api/auth/register/', data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        login_resp = self.client().post('/api/auth/login/', data=self.user_data)
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn("You logged in successfully", str(login_resp.data))

    def test_failed_login(self):
        """Test non registered users cannot login."""
        not_a_user = {
            'email': 'not_a_user@example.com',
            'password': 'nope'
        }
        res = self.client().post('/api/auth/login/', data=not_a_user)
        self.assertEqual(res.status_code, 401)
        self.assertIn("Invalid Email or Password, Please Try again", str(res.data))

    def test_duplicate_emails(self):
        """Test that a user cannot be registered twice."""
        self.client().post('/api/auth/register/', data=self.user_data)
        resp_2 = self.client().post('/api/auth/register/', data=self.user_data)
        self.assertEqual(resp_2.status_code, 202)
        self.assertIn("User already exists. Please login", str(resp_2.data))

    def test_user_logout(self):
        """Test that a user can logout"""
        self.client().post('/api/auth/register/', data=self.user_data)
        result = self.client().post('/api/auth/login/', data=self.user_data)
        #obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        logout = self.client().post(
            '/api/auth/logout/',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(logout.status_code, 200)
        self.assertIn("succesfully logged out", str(logout.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
