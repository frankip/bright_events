"""
This files test the error handling functionality
"""
from __future__ import absolute_import

import unittest
import json
from app import app, db

# local imports
from config import app_config

class TestErrorHandling(unittest.TestCase):
    """Test for error handling in the app"""

    def setUp(self):
        """Set up test variables."""
        self.app = app
        self.app.config.from_object(app_config['testing'])
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_page_not_found(self):
        """ Test error handling for 404 error"""
        resp = self.client().get('/api/events/{}'.format(1))
        self.assertEqual(resp.status_code, 404)
        result = json.loads(resp.data.decode())['message']
        self.assertEquals(result, 'This resource does not exist.')

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
