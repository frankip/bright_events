"""
this files contains the logic and the routes of the app
"""
from flask import request, url_for, abort, session
from flask_api import status, exceptions
from flasgger import Swagger
from flasgger.utils import swag_from

from app import app
from . models import Users, Events
swagger = Swagger(app)


@app.route('/api/auth/register/', methods=['POST'])
def registration():
    """user registration endpoint
          registers a user and takes in a name, email and password
     ---
        tags:
          - Bright Events API
        parameters:
          - in: formData
            name: name
            type: string
            required: true
            description: Enter a name to register!
          - in: formData
            name: email
            type: string
            required: true
            description: The email address you will use to log in!
          - in: formData
            name: password
            type: string
            required: true
            description: The password you will use to registert!
        responses:
          201:
            description: User has been created successfully 
            schema:
              $ref: '#/definitions/Task'
            examples:
                name: John Doe
                email: test@test.com
                password: password
    """
    if "user" in session:
        return {"message": "you are already logged in"}
    fname = request.data.get('first_name')
    lname = request.data.get('last_name')
    email = request.data.get('email')
    password = request.data.get('password')

    if email is None or password is None:
        abort(400)
    user = Users(fname, lname, email, password)
    if email in Users.user_db.keys():
        message = {"message": "User already exists. Please login."}
        return message, status.HTTP_202_ACCEPTED
    user.save()
    return {'message': "user has been created"}, status.HTTP_201_CREATED

@app.route('/api/auth/login/', methods=['POST'])
def login():
    """User login endpoint
        logs in a user created in the register endpoint
    ---
        tags:
          - Bright Events API
        parameters:
          - in: formData
            name: email
            type: string
            required: true
            description: email addres you registered with!
          - in: formData
            name: password
            type: string
            required: true
            description: The password you registered with!
        responses:
          200:
            description: You have logged in successfully 
            schema:
              $ref: '#/definitions/Task'
            examples:
                email: test@test.com
                password: password
    """
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
        print(Users.user_db[email])
        if Users.user_db[email] == password:
            session['user'] = email
            return {
                'message': 'you have succesfully been logged in'}, status.HTTP_200_OK
        else:
            raise exceptions.AuthenticationFailed()
    raise exceptions.AuthenticationFailed()

@app.route('/api/auth/logout/', methods=['POST'])
def logout():
    """User Logout endpoints
        logs out a user
    ---
        tags:
            - Bright Events API
        responses:
            200:
                description: you have been logged out
    """
    if 'user' not in session:
        message = {"message": "you have to login first"}
        return message, status.HTTP_401_UNAUTHORIZED
    session.pop('user')
    message = {"message": "you have been logged out"}
    return message, status.HTTP_200_OK

@app.route('/api/auth/reset-password/', methods=['POST'])
def reset_password():
    """Reset user Password endpoint
        takes in a password and resets the password
    ---
        tags:
          - Bright Events API
        parameters:
          - in: formData
            name: password
            required: true
            description: The password you want to reset!
            type: string
        responses:
          201:
            description: Password updated successfully
            schema:
              $ref: '#/definitions/Task'
            examples:
                password: password

    """
    if 'user' in session:
        password = request.data.get('password')
        Users.user_db['user'] = password
        print(Users.user_db['user'])
        return {"message": "you have succesfuly reset your password"}
    return {"message": "you need to log in first to reset password"}

@app.route("/api/events/", methods=['GET', 'POST'])
@swag_from('flasgger/event_get.yml',  methods=['GET'])
@swag_from('flasgger/event_post.yml',  methods=['POST'])
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
        message = {
            "message": "event created",
             "object": api_view(ids_)}
        return message, status.HTTP_201_CREATED

    # request.method == 'GET'
    return [api_view(ids_) for ids_ in sorted(Events.events_db.keys())]

@app.route("/api/events/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
@swag_from('flasgger/event_details_get.yml',  methods=['GET'])
@swag_from('flasgger/event_details_put.yml',  methods=['PUT'])
@swag_from('flasgger/event_details_delete.yml',  methods=['DELETE'])
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
@swag_from('flasgger/event_rsvp_get.yml',  methods=['GET'])
@swag_from('flasgger/event_rsvp_post.yml',  methods=['POST'])
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
        return {'message': "email added to RSVP", "object": rsvp_list}, status.HTTP_201_CREATED
    return rsvp_list


def api_view(key):
    """Handles how the data will be in the browsable api"""
    return {
        'rsvp_url': request.host_url.rstrip('/') + url_for('rsvp_event', key=key),
        'url': request.host_url.rstrip('/') + url_for('events_details', key=key),
        'event': Events.events_db[key],
    }
