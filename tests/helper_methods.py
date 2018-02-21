"""
This files test the events end point functionality
"""
from __future__ import absolute_import

import unittest
import json
from config import app_config
from app import app, db

class Helper():
    """This class represents the Events test case"""

    def setUp(self):
        """Set up test variables."""
        self.app = app
        self.app.config.from_object(app_config['testing'])
        self.client = self.app.test_client
        self.new_event = {
            "event": "Barbecue party",
            "location": "nairobi",
            "category": "Food",
            "date": "12/12/2017"
        }
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def get_auth_token(self):
        """Helper method to register and login user and get access token"""
        user_data = {
            'first_name': 'new',
            'last_name': 'user',
            'email': 'frank@test.com',
            'password': 'Test_password1'
        }
        #register a user then log them in
        self.client().post('/api/auth/register/', data=user_data)
        result = self.client().post('/api/auth/login/', data=user_data)
        #obtain the access token
        return json.loads(result.data.decode())['access_token']

    def create_event(self):
        """Helper method to create an event"""
        access_token = self.get_auth_token()
        return self.client().post(
            '/api/events/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.new_event)
        

if __name__ == '__main__':
    unittest.main()
