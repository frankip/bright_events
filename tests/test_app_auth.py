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
            'password': 'Test_password1'
            }
        # Binds app to current context
        with self.app.app_context():
            #create all tables
            db.create_all()

    def test_user_registration(self):
        """Test user registration works correcty."""
        resp = self.client().post('/api/auth/register/', data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        result = json.loads(resp.data.decode())['message']
        self.assertIn(result, 'user has been created')

    def test_user_login(self):
        """Test registered user can login."""
        resp = self.client().post('/api/auth/register/', data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        login_resp = self.client().post('/api/auth/login/', data=self.user_data)
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn("You logged in successfully", str(login_resp.data))

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
        result = json.loads(logout.data.decode())['message']
        self.assertIn(result, "succesfully logged out")

    def test_reset_password(self):

        self.client().post('/api/auth/register/', data=self.user_data)
        result = self.client().post('/api/auth/login/', data=self.user_data)
        #obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        reset = self.client().put(
            '/api/auth/reset-password/', 
            headers=dict(Authorization="Bearer " + access_token),
            data={'password': 'Test_password123'})
        self.assertEqual(reset.status_code, 200)
        result = json.loads(reset.data.decode())['message']
        self.assertIn(result, "you have succesfuly reset your password")
        new_login = self.client().post(
            '/api/auth/login/', 
            data={'email': 'test@example.com', 'password': 'Test_password123'})
        self.assertEqual(new_login.status_code, 200)
        result = json.loads(new_login.data.decode())['message']
        self.assertIn(result, "You logged in successfully.")

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
