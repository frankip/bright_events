"""
This files handles all the database logic and instances
"""
import jwt
from datetime import datetime, timedelta
from passlib.apps import custom_app_context as pwd_context

from app import db

class Users(db.Model):
    """
    This class handles all the logic and methods
    associated with a user
    """

    __tablename__ = 'user_db'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    fname = db.Column(db.String(256), nullable=False)
    lname = db.Column(db.String(256), nullable=False)
    event = db.relationship(
        'Events', order_by='Events.id', cascade="all, delete-orphan"
    )

    def __init__(self, fname, lname, email, password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password

    def save(self):
        """Creates a new user and saves to the database"""
        db.session.add(self)
        db.session.commit()

    def check_user(self, email):
        """
        This method takes in a email and
        checks if its in the dictonary
        """
        # if email in self.user_db.keys():
        #     return "User already exists. Please login.", 201
        # return False
        pass

    def hash_password(self, password):
        """
        hash pasword to store in db
        """

        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        """
        check pasword provided with hash in db
        """
        return pwd_context.verify(self.password, password, )

    def generate_token(self, user_id):
        """Generating the access token"""
        try:
            #set up payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('secret'),
                algorithim='HS256'
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
            # The token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            #The token is invalid, return an error string
            return "Invalid token. Please register or login"

class Events(db.Model):
    """
    This class hold the logic and methods for the
    events
    """

    __tablename__ = 'events_db'

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(255))
    location = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(Users.id))



    def __init__(self, event, location, date, created_by):
        self.event = event
        self.location = location
        self.date = date
        self.created_by = created_by
        self.rsvp = []

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        return Events.query.filter_by(created_by=user_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Events: {}>".format(self.event)
