from flask_bcrypt import Bcrypt
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
            return True
        else:
            return False

    def verify_password(self, password):
        '''
        check pasword provided with hash in db
        '''
        return Bcrypt().check_password_hash(self.password, password)

    @staticmethod    
    def is_active(self):
        return True
