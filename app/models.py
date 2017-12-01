from datetime import datetime, timedelta
import itertools
import jwt
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from passlib.apps import custom_app_context as pwd_context
from flask import current_app

from app import app
class Users:
    """
    This class handles all the logic and methods
    associated with a user
    """
    user_db = {}
    id_generator = itertools.count(1)
    def __init__(self, username, password):
        self.id = next(self.id_generator)
        self.username = username
        self.password = password
        
    def save(self):
        '''Saves the data to the datastructure dictonary'''
        # self.user_db[self.id] = {self.username:self.password}
        self.user_db[self.username] = self.password
        return self

    def check_user(self, username):
        '''
        This method takes in a username and
        checks if its in the dictonary
        '''
        if username in self.user_db.keys():
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

    def generate_token(self, user_id):
        """Generates the access token to be used as the Authorization header"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        '''Decodes the access token from the Authorization header.'''
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"


    @staticmethod
    def verify_auth_token(token):
        '''verifies the access token from the Authorization header'''
        s = Serializer(app.config.from_object('config'))
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        # user = User.query.get(data['id'])
        # return user

    @staticmethod    
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

