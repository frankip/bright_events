"""This file tests for the model class functionality"""
from __future__ import absolute_import
from unittest import TestCase

# local imports
from app.models import (
    Users,
    BlackListToken,
    Events
)
from app import db

class UsersTestCase(TestCase):
    """Test Users class functionality"""

    def setUp(self):
        self.user = Users

    def test_user_creation(self):
        """Test user creation"""
        new_user = self.user('John','Doe', 'john.doe@self.com', 'password')
        pass
        # saved = new_user.save()
        # self.assertEquals()
