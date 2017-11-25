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
        print(password)
        self.password = pwd_context.encrypt(password)
        print (self.password)

    def verify_password(self, password):
        '''
        check pasword provided with hash in db
        '''
        return pwd_context.verify(password, self.password)

    @staticmethod    
    def is_active(self):
        return True
