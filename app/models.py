"""
This files handles all the database logic and instances
"""
import itertools
from passlib.apps import custom_app_context as pwd_context

from app import db

class Users:
    """
    This class handles all the logic and methods
    associated with a user
    """
    user_db = {}
    id_generator = itertools.count(1)

    def __init__(self, fname, lname, email, password):
        self._id = next(self.id_generator)
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password

    def save(self):
        """Saves the data to the datastructure dictonary"""
        self.user_db[self._id] = dict(
            fname=self.fname,
            lname=self.lname,
            email=self.email,
            password=self.password
        )
        self.user_db[self.email] = self.password
        return self

    def check_user(self, email):
        """
        This method takes in a email and
        checks if its in the dictonary
        """
        if email in self.user_db.keys():
            return "User already exists. Please login.", 201
        return False

    def hash_password(self, password):
        """
        hash pasword to store in db
        """

        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        """
        check pasword provided with hash in db
        """
        pass
        # return pwd_context.verify(password, self.password)


class Events():
    """
    This class hold the logic and methods for the
    events
    """
    # events_db = {}
    # id_generator = itertools.count(1)

    __tablename__ = 'events_db'

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(255))
    location = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=db.func.current_timestamp())



    def __init__(self, event, location, date):
        self.event = event
        self.location = location
        self.date = date
        self.rsvp = []

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return events_db.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Events: {}>".format(self.event)

    # def add_event(self):
    #     """handles adding events to dictonary"""
    #     new_data = dict(
    #         event=self.event,
    #         location=self.location,
    #         date=self.date,
    #         rsvp=self.rsvp
    #     )
    #     self.events_db[self.ids_] = new_data
    #     return self.ids_
