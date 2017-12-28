"""
this files contains the logic and the routes of the app
"""
import re
from flask import request, url_for, session, jsonify
from flask_api import status, exceptions
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flasgger.utils import swag_from

#local imports
from app import app
from . models import Users, Events

# initialize sql-alchemy
db = SQLAlchemy()

#flassger api documentation
Swagger(app)


@app.route('/api/auth/register/', methods=['GET', 'POST'])
@swag_from('flasgger/auth_registration.yml', methods=['POST'])
def registration():
    """
    user registration endpoint registers a user and
    takes in a first name, last name, email, and password
    """
    if "user" in session:
        message = {"message": "you are already logged in"}
        return message, status.HTTP_202_ACCEPTED

    # Retrieve data from the user side
    fname = request.data.get('first_name')
    lname = request.data.get('last_name')
    email = request.data.get('email')
    password = request.data.get('password')

    """
    validating the data from user isalpha ensures there are no
    non-alphabet characters
    """

    if fname is None or fname.strip == "" or not fname.isalpha():
        message = {"message": "ensure the first name is not empty or filled out correctly"}
        return message, status.HTTP_400_BAD_REQUEST


    if lname is None or lname.strip == "" or not lname.isalpha():
        message = {"message": "ensure the last name is not empty or filled out correctly"}
        return message, status.HTTP_400_BAD_REQUEST

    if email is None or email.strip == "" or not re.search(
            r'[\w.-]+@[\w.-]+.\w+', email):
        message = {"message": "ensure that email is not empty or filled out correctly"}
        return message, status.HTTP_400_BAD_REQUEST

    if password is None:
        message = {"message": "Password can not be empty"}
        return message, status.HTTP_400_BAD_REQUEST

    # instantiate a user from the user class
    user = Users(fname, lname, email, password)

    # check if the user is already registered
    if email in Users.user_db.keys():
        message = {"message": "User already exists. Please login."}
        return message, status.HTTP_202_ACCEPTED

    # if new user save them to the database
    user.save()
    message = {'message': "user has been created"}
    return message, status.HTTP_201_CREATED


@app.route('/api/auth/login/', methods=['POST'])
@swag_from('flasgger/auth_login.yml', methods=['POST'])
def login():
    """User login endpoint logs in a user created in the register endpoint"""
    email = request.data.get('email')
    password = request.data.get('password')

    if email is None or password is None:
        message = {'message': 'inputs cannot be empty'}
        return message, status.HTTP_400_BAD_REQUEST

    if not Users.user_db.keys():
        message = {"message": "You need to register first before you login"}
        return message, status.HTTP_400_BAD_REQUEST

    # user = Users(email, password)
    if email in Users.user_db.keys():
        if Users.user_db[email] == password:
            session['user'] = email
            message = {'message': 'you have successfully been logged in'}
            return message, status.HTTP_200_OK
        else:
            raise exceptions.AuthenticationFailed()
    raise exceptions.AuthenticationFailed()


@app.route('/api/auth/logout/', methods=['POST'])
@swag_from('flasgger/auth_logout.yml', methods=['POST'])
def logout():
    """User Logout endpoints logs out a user"""
    if 'user' not in session:
        message = {"message": "you have to login first"}
        return message, status.HTTP_401_UNAUTHORIZED
    session.pop('user')
    message = {"message": "you have been logged out"}
    return message, status.HTTP_200_OK


@app.route('/api/auth/reset-password/', methods=['POST'])
@swag_from('flasgger/auth_reset_password.yml', methods=['POST'])
def reset_password():
    """Reset user Password endpoint takes in a password and resets the password"""
    if 'user' in session:
        password = request.data.get('password')
        Users.user_db['user'] = password
        message = {"message": "you have succesfuly reset your password"}
        return message, status.HTTP_200_OK
    message = {"message": "you need to log in first to reset password"}
    return message, status.HTTP_401_UNAUTHORIZED


@app.route("/api/events/", methods=['GET', 'POST'])
@swag_from('flasgger/event_get.yml', methods=['GET'])
@swag_from('flasgger/event_post.yml', methods=['POST'])
def events_list():
    """List or create events."""
    if request.method == 'POST':
        event = request.data.get('event')
        location = request.data.get('location')
        date = request.data.get('date')

        if event is None or location is None or date is None:
            message = {'message': 'inputs cannot be empty, please fill all inputs'}
            return message, status.HTTP_400_BAD_REQUEST

        inst = Events(event, location, date)
        inst.save()
        # ids_ = inst.add_event()
        response = jsonify({
            'id': inst.id,
            'event': inst.event,
            'location': inst.location,
            'date': inst.date
        })

        # message = {
        #     "message": "event created",
        #     "object": response}
        return response, status.HTTP_201_CREATED

    # request.method == 'GET'
    return [api_view(ids_) for ids_ in sorted(Events.events_db.keys())]


@app.route("/api/events/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
@swag_from('flasgger/event_details_get.yml', methods=['GET'])
@swag_from('flasgger/event_details_put.yml', methods=['PUT'])
@swag_from('flasgger/event_details_delete.yml', methods=['DELETE'])
def events_details(key):
    """Retrieve, update or delete events instances."""
    if key not in Events.events_db:
        raise exceptions.NotFound()

    if request.method == 'PUT':
        event = request.data.get('event')
        location = request.data.get('location')
        date = request.data.get('date')

        if event is None or location is None or date is None:
            return {'message': 'inputs cannot be empty, please fill all inputs'}

        new_dat = dict(
            event=event,
            location=location,
            date=date
        )
        Events.events_db[key] = new_dat
        message = {"message": "event updated", "object": api_view(key)}
        return message, status.HTTP_201_CREATED

    elif request.method == "DELETE":
        Events.events_db.pop(key, None)
        message = {"message": "Deleted succesfully"}
        return message, status.HTTP_204_NO_CONTENT

    return api_view(key)


@app.route("/api/events/<int:key>/rsvp/", methods=['GET', 'POST'])
@swag_from('flasgger/event_rsvp_get.yml', methods=['GET'])
@swag_from('flasgger/event_rsvp_post.yml', methods=['POST'])
def rsvp_event(key):
    """ Handles the RSVP logic"""
    if key not in Events.events_db:
        raise exceptions.NotFound()

    events = Events.events_db[key]
    rsvp_list = events['rsvp']
    if request.method == "POST":
        email = request.data.get('email')
        if email is None:
            return{"message": "can not rsvp empty inputs"}
        rsvp_list.append(email)
        return {'message': "email added to RSVP",
                "object": rsvp_list}, status.HTTP_201_CREATED
    return rsvp_list


def api_view(key):
    """Handles how the data will be in the browsable api"""
    return {
        'rsvp_url': request.host_url.rstrip('/') + url_for('rsvp_event', key=key),
        'url': request.host_url.rstrip('/') + url_for('events_details', key=key),
        'event': Events.events_db[key],
    }
