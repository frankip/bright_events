"""
This file covers the test cases for 
the events functionality
"""
import unittest

import os
from app import app

class TestEventsItem(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.new_event = {"text": "andela bootcamp"}
        
    def test_retrieve_events(self):
        resp = self.client().post('/api/events', data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().get('/api/events')
        self.assertIn('andela bootcamp', str(resp.data))

    def test_create_event(self):
        resp = self.client().post('/api/events', data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('andela bootcamp', str(resp.data))
    
    def test_update_event(self):
        resp = self.client().post('api/events', data=self.new_event)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().put('/api/events/1/', 
                data={"text":"andela bootcamp cohort 24"})
        self.assertEqual(resp.status_code, 200)
        new_ = self.client().get('api/events/1/')
        self.assertIn('cohort', str(new_.data))


if __name__ == '__main__':
    unittest.main()

