import itertools
import jwt
from datetime import datetime, timedelta
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from passlib.apps import custom_app_context as pwd_context
from flask import abort, current_app

from app import app
class Users:
    user_db = {}
    id_generator = itertools.count(1)
    def __init__(self, username, password):
        self.id = next(self.id_generator)
        self.username = username
        self.password = password
        

    def save(self):
        # self.user_db[self.id] = {self.username:self.password}
        self.user_db[self.username] = self.password
        return self

    def check_user(self, username):
        '''
        This method takes in a username and
        checks if its in the dictonary
        '''
        if username in self.user_db.keys():
            return abort(400)
        else:
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
        """Decodes the access token from the Authorization header."""
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
        s = Serializer(app.config.from_object('config'))
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    @staticmethod    
    def is_active(self):
        return True

<<<<<<< HEAD
class Events():
    events_db = {}
=======

class Events():
    events_db = {}

>>>>>>> 829c1eb50e91c597ce84a28be13be356b270e209
    def __init__(self, name):
        self.name = name
        self.rsvp = []

    def add_event(self):
        if not self.events_db.keys():
            ids_ = 0
        else:
            ids_ = max(self.events_db.keys()) + 1

        self.events_db[ids_] = self.name
<<<<<<< HEAD

        return api_view(ids_) 

    def api_view():
        pass
    # """
    # Handles how the data will be 
    # in the browsable api
    # """
    # return {
    # 'name': self.events_db.keys(),
    # 'url': request.host_url.rstrip('/') + url_for('events_details', key=key)
    # }
=======
        return ids_
>>>>>>> 829c1eb50e91c597ce84a28be13be356b270e209
