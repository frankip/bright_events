"""
This files test the events end point functionality
"""
from __future__ import absolute_import

import unittest
from app import app
class TestEventsItem(unittest.TestCase):
    """This class represents the Events test case"""
    def setUp(self):
        """Set up test variables."""
        self.app = app
        self.client = self.app.test_client
        self.new_event = {"event": "Barbecue party",
                          "location": "nairobi",
                          "date": "12/12/2017"
                         }
        self.updat_event = {"event": "Burger Fest",
                            "location": "nairobi",
                            "date": "12/12/2017"
                           }
    def test_retrieve_events(self):
        """Test API can retrieve events (GET request)."""
        resp = self.client().post('/api/events', data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().get('/api/events')
        self.assertIn('Barbecue', str(resp.data))

    def test_create_event(self):
        """Test API can create an event (POST request)"""
        resp = self.client().post('/api/events', data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Barbecue party', str(resp.data))

    def test_update_event(self):
        """Test API can edit an existing event. (PUT request)"""
        resp = self.client().post('api/events', data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().put('/api/events/1/',
                                 data=self.updat_event)
        self.assertEqual(resp.status_code, 201)
        new_ = self.client().get('api/events/1/')
        self.assertIn('Burger', str(new_.data))

    def test_event_deletion(self):
        """Test API can delete an existing event. (DELETE request)."""
        resp = self.client().post('/api/events', data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        res = self.client().delete('/api/events/1/')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/api/events/1/')
        self.assertEqual(result.status_code, 404)




if __name__ == '__main__':
    unittest.main()

