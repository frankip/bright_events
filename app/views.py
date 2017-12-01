"""
this files contains the logic and the routes of the app
"""
from flask import request, url_for, abort, g, jsonify, session
from flask_api import status, exceptions

from app import app
from . models import Users, Events

@app.route('/api/auth/register', methods=['POST'])
def registration():
    """ This function handles the user registration"""
    email = request.data.get('email')
    password = request.data.get('password')

    if email is None or password is None:
        abort(400)
    user = Users(email, password)
    if email in Users.user_db.keys():
        message = {"message": "User already exists. Please login."}
        return message , status.HTTP_202_ACCEPTED
    user.save()
    return {'message': "user has been created"}, status.HTTP_201_CREATED

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Handles the user login logic """
    username = request.json.get('username')
    password = request.json.get('password')


    if username is None or password is None:
        message = {'message': 'inputs cannot be empty'}
        return message , status.HTTP_400_BAD_REQUEST

    if not Users.user_db.keys():
        message = {"message": "You need to register first before you login"}
        return message, status.HTTP_400_BAD_REQUEST

    user = Users(username, password)
    if username in Users.user_db.keys():
        if Users.user_db[username] == password:
            g.user = user
            session['user'] = g.user.username
            return {'message': 'you have succesfully been logged in'}, status.HTTP_200_OK
        else:
            raise exceptions.AuthenticationFailed()
    raise exceptions.AuthenticationFailed()

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Handles the user logout logic"""
    if 'user' not in session:
        message = {"message": "you have to login first"}
        return message , status.HTTP_401_UNAUTHORIZED
    session.pop('user')
    message = {"message": "you have been logged out"}
    return message , status.HTTP_200_OK

# app.route('/api/auth/reset-password', methods=['POST'])
# def reset_password():

def api_view(key):
    """Handles how the data will be in the browsable api"""
    return {
        'rsvp_url': request.host_url.rstrip('/') + url_for('rsvp_event', key=key),
        'url': request.host_url.rstrip('/') + url_for('events_details', key=key),
        'event': Events.events_db[key],
    }

@app.route("/api/events", methods=['GET', 'POST'])
def events_list():
    """List or create events."""
    if request.method == 'POST':
        event = request.data.get('event')
        location = request.data.get('location')
        date = request.data.get('date')
        
        if event is None or location is None or date is None:
            return {'message': 'inputs cannot be empty, please fill all inputs'}

        inst = Events(event, location, date)
        ids_ = inst.add_event()
        message = {"message": api_view(ids_)}
        return message, status.HTTP_201_CREATED

    # request.method == 'GET'
    return [api_view(ids_) for ids_ in sorted(Events.events_db.keys())]

@app.route("/api/events/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def events_details(key):
    """Retrieve, update or delete events instances."""
    if request.method == 'PUT':
        name = str(request.data.get('text', ''))
        location = str(request.data.get('location', ''))
        date = str(request.data.get('date', ''))
        new_dat = dict(
            name=name,
            location=location,
            date=date
        )
        Events.events_db[key] = new_dat
        message = {"message": api_view(key)}
        return message, status.HTTP_201_CREATED

    elif request.method == "DELETE":
        Events.events_db.pop(key, None)
        message = {"message": "Deleted succesfully"}
        return message, status.HTTP_204_NO_CONTENT

    if key not in Events.events_db:
        raise exceptions.NotFound()
    return api_view(key)


@app.route("/api/events/<int:key>/rsvp", methods=['GET', 'POST'])
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
        return {'message':rsvp_list}, status.HTTP_201_CREATED
    return rsvp_list
