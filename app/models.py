"""
This files handles all the database logic and instances
"""
import itertools
from passlib.apps import custom_app_context as pwd_context
class Users:
    """
    This class handles all the logic and methods
    associated with a user
    """
    user_db = {}
    id_generator = itertools.count(1)
    def __init__(self, email, password):
        self._id = next(self.id_generator)
        self.email = email
        self.password = password
        
    def save(self):
        '''Saves the data to the datastructure dictonary'''
        # self.user_db[self.id] = {self.username:self.password}
        self.user_db[self.email] = self.password
        return self

    def check_user(self, email):
        '''
        This method takes in a username and
        checks if its in the dictonary
        '''
        if email in self.user_db.keys():
            return "User already exists. Please login.", 201
        return False
    def hash_password(self, password):
        '''
        hash pasword to store in db
        '''

        self.password = pwd_context.encrypt(password)
    def verify_password(self, password):
        '''
        check pasword provided with hash in db
        '''
        pass
        # return pwd_context.verify(password, self.password)

    # @staticmethod    
    def is_active(self):
        '''sets the is active flag to true'''
        return True
class Events():
    '''
    This class hold the logic and methods for the
    events
    '''
    events_db = {}
    id_generator = itertools.count(1)

    def __init__(self, name, location, date):
        self.ids_ = next(self.id_generator)
        self.name = name
        self.location = location
        self.date = date
        self.rsvp = []

    def add_event(self):
        '''handles adding events to dictonary'''
        new_data = dict(
            name=self.name,
            location=self.location,
            date=self.date,
            rsvp=self.rsvp
        )
        self.events_db[self.ids_] = new_data
        return self.ids_

