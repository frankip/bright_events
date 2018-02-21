"""
This files test the event details functionality
"""
from __future__ import absolute_import

import unittest
import json
from app import app, db

# local imports
from config import app_config
from .helper_methods import Helper

class TestEventsDetails(unittest.TestCase, Helper):
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

    def test_retrieve_single_event(self):
        """Test API can retrieve a single event by using it's id.(GET request)."""
        access_token = self.get_auth_token()
        resp = self.create_event()
        self.assertEqual(resp.status_code, 201)
        result = self.client().get(
            '/api/events/{}/'.format(1),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Barbecue', str(result.data))

    def test_failed_retrieve_single_event(self):
        """Test retrieving non existing event"""
        resp = self.client().get('/api/events/{}/'.format(3))
        result = json.loads(resp.data.decode())['message']
        self.assertEquals(result, 'This resource does not exist.')

    def test_update_event(self):
        """Test API can edit an existing event. (PUT request)"""
        access_token = self.get_auth_token()
        resp = self.create_event()
        self.assertEqual(resp.status_code, 201)
        resp = self.client().put(
            'api/events/{}/'.format(1),
            headers=dict(Authorization="Bearer " + access_token),
            data=self.update_event)
        self.assertEqual(resp.status_code, 201)
        result = json.loads(resp.data.decode())['event']
        self.assertEquals(result, 'Burger Fest')
        new_ = self.client().get(
            'api/events/{}/'.format(1),
            headers=dict(Authorization="Bearer " + access_token))
        result = json.loads(new_.data.decode())['event']
        self.assertEquals(result, 'Burger Fest')

    def test_event_deletion(self):
        """Test API can delete an existing event. (DELETE request)."""
        access_token = self.get_auth_token()
        resp = self.create_event()
        self.assertEqual(resp.status_code, 201)
        res = self.client().delete(
            '/api/events/{}/'.format(1),
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get(
            '/api/events/{}/'.format(1),
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

         
