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
        user_data = {'username': 'test.com',
                     'password': 'test_password'
                     }
        """Test user registration works correcty."""
        resp = self.client().post('/api/auth/register', data=user_data)
        self.assertEqual(resp.status_code, 201)
        result = json.loads(resp.data.decode())
        self.assertEqual(result['username'], "test.com")
    
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
        # result = json.dumps(resp_2.data.decode())
        # self.assertEqual(result['message'], "User already exists. Please login.")


if __name__ == '__main__':
    unittest.main()
