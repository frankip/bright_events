"""
This files test the event rsvp functionality
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

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_rsvp_to_an_event(self):
        """Test API can RSVP to an event (POST request)"""
        access_token = self.get_auth_token()
        resp = self.create_event()
        self.assertEqual(resp.status_code, 201)
        res = self.client().post(
            'api/events/1/rsvp/',
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(res.status_code, 201)
        self.assertIn(
            'Thank you for registering to attend this event', str(res.data))

    def test_rsvp_to_an_event_more_than(self):
        """Test API can not rsvp more than once to an event (POST request)"""
        access_token = self.get_auth_token()
        resp = self.create_event()
        self.assertEqual(resp.status_code, 201)
        res = self.client().post(
            'api/events/1/rsvp/',
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(res.status_code, 201)
        new_res = self.client().post(
            'api/events/{}/rsvp/'.format(1),
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(new_res.status_code, 202)
        self.assertIn("You have already RSVP", str(new_res.data))
        
    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
