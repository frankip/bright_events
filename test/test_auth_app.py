"""
This files test the Authentication endpoints functionality
"""
from __future__ import absolute_import

import unittest
import json
from app import app


class UserAuthTestcase(unittest.TestCase):
    """Test case for the authentication functionality."""

    def setUp(self):
        """Set up test variables."""
        self.app = app
        self.client = self.app.test_client
        self.user_data = {
            'email': 'test@example.com',
            'password': 'test_password'
            }

    def test_user_registration(self):
        """Test user registration works correcty."""
        user_data = {
            'email': 'test.com',
            'password': 'test_password'
            }
        resp = self.client().post('/api/auth/register', data=user_data)
        self.assertEqual(resp.status_code, 201)
        result = json.loads(resp.data.decode())
        self.assertEqual(result['message'], "user has been created")

    def test_user_login(self):
        """Test registered user can login."""
        self.user_data = {
            'email': 'frank@example.com',
            'password': 'test_password'
            }
        resp = self.client().post('/api/auth/register', data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        login_resp = self.client().post('/api/auth/login', data=self.user_data)
        self.assertEqual(login_resp.status_code, 200)

    def test_failed_login(self):
        """Test non registered users cannot login."""
        not_a_user = {
            'email': 'not_a_user@example.com',
            'password': 'nope'
        }
        res = self.client().post('/api/auth/login', data=not_a_user)
        self.assertEqual(res.status_code, 401)

    def test_duplicate_usernames(self):
        """Test that a user cannot be registered twice."""
        resp = self.client().post('/api/auth/register', data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        resp_2 = self.client().post('/api/auth/register', data=self.user_data)
        self.assertEqual(resp_2.status_code, 202)


if __name__ == '__main__':
    unittest.main()
