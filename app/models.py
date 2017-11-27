from passlib.apps import custom_app_context as pwd_context
from flask import abort
class Users:
    user_db = {}
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
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

    @staticmethod    
    def is_active(self):
        return True

class Events():
    events_db = {}
    def __init__(self, name):
        self.name = name
        self.rsvp = []

    def add_event(self):
        if not self.events_db.keys():
            ids_ = 0
        else:
            ids_ = max(self.events_db.keys()) + 1

        self.events_db[ids_] = self.name

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
