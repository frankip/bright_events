"""
This files handles all the database logic and instances
"""
from datetime import datetime, timedelta
import jwt
from passlib.apps import custom_app_context as pwd_context

from app import db, app

#association table that associates userstable to events table
rsvp = db.Table('rsvps',
                db.Column('user_id', db.Integer, db.ForeignKey('user_db.id')),
                db.Column('event_id', db.Integer,
                          db.ForeignKey('events_db.id'))
               )
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
    event_rsvp = db.relationship(
        'Events', secondary=rsvp, backref=db.backref('rsvp', lazy='dynamic')
    )

    def __init__(self, fname, lname, email, password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = pwd_context.encrypt(password)

    def save(self):
        """Creates a new user and saves to the database"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check_user(email):
        """
        This method takes in a email and
        checks if its in the database
        """
        return Users.query.filter_by(email=email).first()

    def verify_password(self, password):
        """
        check pasword provided with hash in db
        """
        return pwd_context.verify(password, self.password)

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
                app.secret_key,
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    def get_full_names(self):
        """Returns the full namesod user"""
        return self.fname +' '+ self.lname

    @staticmethod
    def decode_token(token):
        '''Decodes the access token from the Authorization header.'''
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, app.secret_key)
            blacklisted_token = BlackListToken.check_black_list(token)
            if blacklisted_token:
                return "You have logged out, Please log in to continue"
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # The token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            #The token is invalid, return an error string
            return "Invalid token. Please register or login"

class BlackListToken(db.Model):
    __tablename__ = 'blacklist_token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.now()

    def logout(self):
        """
        add the blacklisted token to database
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check_black_list(token):
        resp = BlackListToken.query.filter_by(token = str(token)).first()

        if resp:
            return True

        return False

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

class Events(db.Model):
    """
    This class hold the logic and methods for the
    events
    """
    __tablename__ = 'events_db'

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(255))
    location = db.Column(db.String(255))
    category = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(Users.id))

    def __init__(self, event, location, category, date, created_by):
        self.event = event
        self.location = location
        self.category = category
        self.date = date
        self.created_by = created_by

    def save(self):
        """
        Save changes to the database
        """
        db.session.add(self)
        db.session.commit()

    def rsvp_user(self, user):
        """
        Add user to the rsvp list
        """
        #Get user object
        usr = Users.query.filter_by(id=user).first()
        self.rsvp.append(usr)
        self.save()

    def already_rsvpd(self, user):
        """
        check if the user has already rsvpd to the event
        """
        return self.rsvp.filter_by(
            id=user).first() is not None

    @staticmethod
    def get_all_user_events(user_id, page):
        """
        Get all the events created by the user
        """
        return Events.query.filter_by(created_by=user_id).paginate(page, 3)

    @staticmethod
    def get_single_event(key):
        """Retrieves a single event"""
        return Events.query.filter_by(id=key).first()

    def delete(self):
        """Removes a record from the database"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Events: {}>".format(self.event)
