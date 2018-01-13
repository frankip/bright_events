"""
This files test the events end point functionality
"""
from __future__ import absolute_import

import unittest
from config import app_config
from app import app,db


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
            "date": "12/12/2017"
        }
        self.update_event = {
            "event": "Burger Fest",
            "location": "Ngong",
            "date": "12/12/2017"
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()


    def test_create_event(self):
        """Test API can create an event (POST request)"""
        resp = self.client().post('/api/events/', data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Barbecue party', str(resp.data))

    def test_retrieve_all_events(self):
        """Test API can retrieve all events (GET request)."""
        resp = self.client().post('/api/events/', data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().get('/api/events/')
        self.assertIn('Barbecue', str(resp.data))


    def test_retrieve_single_event(self):
        """Test API can retrieve a single event by using it's id.(GET request)."""
        resp = self.client().post('/api/events/', data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        result = self.client().get(
            '/api/events/{}/'.format(1))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Barbecue', str(result.data))

    def test_update_event(self):
        """Test API can edit an existing event. (PUT request)"""
        resp = self.client().post('api/events/', data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().put('api/events/1/', data=self.update_event)
        self.assertEqual(resp.status_code, 201)
        new_ = self.client().get('api/events/1/')
        self.assertIn('Burger', str(new_.data))

    def test_event_deletion(self):
        """Test API can delete an existing event. (DELETE request)."""
        resp = self.client().post('/api/events/', data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        res = self.client().delete('/api/events/1/')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/api/events/1/')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
    
