from __future__ import absolute_import

import unittest
import json
from app import app
class UserAuthTestcase(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.user_data = {'username': 'test@example.com',
            'password': 'test_password'
        }

    def test_user_registration(self):
        """Test user registration works correcty."""
        # resp = self.client().post('/api/auth/register', data=self.user_data)
        # self.assertEqual(resp.status_code, 201)
        # result = json.loads(resp.data.decode())
        # self.assertEqual(result['message'], "you registered succesfully")
    
    def test_user_login(self):
        pass

    def test_failed_login(self):
        pass

    def test_duplicate_usernames(self):
        """Test that a user cannot be registered twice."""
        resp = self.client().post('/api/auth/register', data=self.user_data)
        self.assertEqual(resp.status_code, 201)
        resp_2 = self.client().post('/api/auth/register', data=self.user_data)
        self.assertEqual(resp_2.status_code, 202)


if __name__ == '__main__':
    unittest.main()
