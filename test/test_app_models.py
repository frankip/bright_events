"""This file tests for the model class functionality"""
from __future__ import absolute_import
from unittest import TestCase

# local imports
from app.models import (
    Users,
    Events
)

class UsersTestCase(TestCase):
    """Test Users class functionality"""

    def setUp(self):
        self.user = Users
        self.password = self.user.hash_password('password')
        self.new_user = self.user(
            'John', 'Doe', 'john.doe@self.com', self.password)

        self.new_event = Events(
            "Barbecue party", "nairobi", "Food", "12/12/2017", 'frank')

    def test_user_creation(self):
        """Test user creation"""
        user = self.new_user
        self.assertIsInstance(user, Users)

    def test_user_returns_full_names(self):
        """Test that user class can return the full names"""
        names = self.new_user.get_full_names()
        self.assertEquals(names, "John Doe")

    def test_user_can_access_all_variables(self):
        """Test to check if all variables are accesible in an instance"""
        user = self.new_user
        self.assertEquals(user.email, 'john.doe@self.com')
        self.assertEquals(user.fname, 'John')
        self.assertEquals(user.lname, 'Doe')

    def test_create_event(self):
        """Test if event class can create event"""
        event = self.new_event
        self.assertIsInstance(event, Events)

    def test_access_events_variables(self):
        """Test that we cann access all vriable from event instance"""
        event = self.new_event
        self.assertEquals(event.event, "Barbecue party")
        self.assertEquals(event.location, "nairobi")
        self.assertEquals(event.category, "Food")
