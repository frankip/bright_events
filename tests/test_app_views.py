"""
This files test the events end point functionality
"""
from __future__ import absolute_import

import unittest
import json
from config import app_config
from app import app, db

from .helper_methods import Helper

class TestEventsItem(unittest.TestCase, Helper):
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

    def test_create_event(self):
        """Test API can create an event (POST request)"""
        resp = self.create_event()
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Barbecue party', str(resp.data))

    def test_retrieve_all_events(self):
        """Test API can retrieve all events (GET request)."""
        resp = self.create_event()
        self.assertEqual(resp.status_code, 201)
        resp = self.client().get(
            '/api/events/')
        self.assertIn('Barbecue', str(resp.data))

    def test_retrieve_all_events_by_user(self):
        """Test if user can retrieve all events he created (GET request)"""
        access_token = self.get_auth_token()
        self.create_event()
        resp = self.client().get(
            '/api/events/',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('Barbecue', str(resp.data))

    def test_category_return_response(self):
        """
        Check if category will not return a null response
        when nothing is provided
        """
        access_token = self.get_auth_token()
        null_category = {
            "event": "Barbecue party",
            "location": "nairobi",
            "date": "12/12/2017"
        }
        empty_category = {
            "event": "Barbecue party",
            "location": "nairobi",
            "category": "",
            "date": "12/12/2017"
        }
        resp = self.client().post(
            '/api/events/',
            headers=dict(Authorization="Bearer " + access_token),
            data=null_category)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().get(
            '/api/events/{}/'.format(1),
            headers=dict(Authorization="Bearer " + access_token))
        result = json.loads(resp.data.decode())['category']
        self.assertEquals(result, 'No Category')
        resp_2 = self.client().post(
            '/api/events/',
            headers=dict(Authorization="Bearer " + access_token),
            data=empty_category)
        self.assertEqual(resp_2.status_code, 201)
        resp_2 = self.client().get(
            '/api/events/{}/'.format(1),
            headers=dict(Authorization="Bearer " + access_token))
        result = json.loads(resp_2.data.decode())['category']
        self.assertEquals(result, 'No Category')

    def test_filter_events(self):
        """Test a user can filter events by location and category"""
        self.create_event()

        # Filter for category in events
        filt_1 = self.client().post(
            '/api/events/search/?category=Food')
        result = json.loads(filt_1.data.decode())[0]
        self.assertEquals(result['category'], "Food")

        # Filter for location in events
        filt_2 = self.client().post('/api/events/search/?location=nairobi')
        result = json.loads(filt_2.data.decode())[0]
        self.assertEquals(result['location'], 'nairobi')

        # Filter for both location and category
        filt_3 = self.client().post(
            'api/events/search/?category=Food&location=nairobi')
        result = json.loads(filt_3.data.decode())[0]
        self.assertEquals(result['location'], 'nairobi')
        self.assertEquals(result['category'], 'Food')

        # filter for non recognized value
        filt_4 = self.client().post(
            'api/events/search/?catey=yadada')
        result = json.loads(filt_4.data.decode())['message']
        self.assertEquals(result, 'That query can not be found')

        # filter for non existing query
        filt_5 = self.client().post('/api/events/search/?location=kiambu')
        result = json.loads(filt_5.data.decode())['message']
        self.assertEquals(result, 'There are no events matching that query')

    def test_invalid_access_token(self):
        """Test invalid access token"""
        access_token = "abcd"
        resp = self.client().post(
            '/api/events/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.new_event)
        self.assertEqual(resp.status_code, 401)
        res = json.loads(resp.data.decode())['message']
        self.assertEquals(res, "Invalid token. Please register or login")

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

