"""
This files test the events end point functionality
"""
from __future__ import absolute_import

import unittest
import json
from config import app_config
from app import app, db


class TestEventsItem(unittest.TestCase):
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
        self.update_event = {
            "event": "Burger Fest",
            "location": "Ngong",
            "category": "Food",
            "date": "12/12/2017"
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def register_user(self):
        """This helper method helps register a test user."""
        user_data = {
            'first_name': 'new',
            'last_name': 'user',
            'email': 'frank@test.com',
            'password': 'test_password'
        }
        return self.client().post('/api/auth/register/', data=user_data)

    def login_user(self):
        """This helper method helps log in a test user."""
        user_data = {
            'email': 'frank@test.com',
            'password': 'test_password'
        }
        return self.client().post('/api/auth/login/', data=user_data)

    def get_auth(self):
        """Helper method to register and login user and get access token"""
        #register a user then log them in
        self.register_user()
        result = self.login_user()
        #obtain the access token
        return json.loads(result.data.decode())['access_token']

    def test_create_event(self):
        """Test API can create an event (POST request)"""
        access_token = self.get_auth()
        resp = self.client().post(
            '/api/events/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Barbecue party', str(resp.data))

    def test_retrieve_all_events(self):
        """Test API can retrieve all events (GET request)."""
        access_token = self.get_auth()
        resp = self.client().post(
            '/api/events/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().get(
            '/api/events/',
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertIn('Barbecue', str(resp.data))

    def test_retrieve_single_event(self):
        """Test API can retrieve a single event by using it's id.(GET request)."""
        access_token = self.get_auth()
        resp = self.client().post(
            '/api/events/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        result = self.client().get(
            '/api/events/{}/'.format(1),
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(result.status_code, 200)
        self.assertIn('Barbecue', str(result.data))

    def test_update_event(self):
        """Test API can edit an existing event. (PUT request)"""
        access_token = self.get_auth()
        resp = self.client().post(
            'api/events/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().put(
            'api/events/1/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.update_event)
        self.assertEqual(resp.status_code, 201)
        new_ = self.client().get(
            'api/events/1/',
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertIn('Burger', str(new_.data))

    def test_event_deletion(self):
        """Test API can delete an existing event. (DELETE request)."""
        access_token = self.get_auth()
        resp = self.client().post(
            '/api/events/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        res = self.client().delete(
            '/api/events/1/',
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get(
            '/api/events/1/',
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
