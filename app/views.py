"""
this files contains the logic and the routes of the app
"""
import re
from flask import request, session
from flask_api import status, exceptions

#local imports
from app import app
from .models import Users, Events, BlackListToken

def authentication_request():
    """Helper class that gets the access token"""
    # Get the access token from the header
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            access_token = auth_header.split(' ')[1]
        except IndexError:
            return {"message": "Token is malformed"}, status.HTTP_401_UNAUTHORIZED
    else:
        access_token = ''

    return access_token


@app.route('/api/auth/register/', methods=['GET', 'POST'])
def registration():
    """
    user registration endpoint registers a user and
    takes in a first name, last name, email, and password
    """
    # Retrieve data from the user side
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    password = request.data.get('password')

    """
    validating the data from user isalpha ensures there are no
    non-alphabet characters
    """

    if first_name is None or first_name.strip == "" or not first_name.isalpha():
        message = {"message": "ensure the first name is not empty and it consist of alphabets only"}
        return message, status.HTTP_400_BAD_REQUEST


    if last_name is None or last_name.strip == "" or not last_name.isalpha():
        message = {
            "message": "ensure the last name is not empty and it consist of alphabets only"}
        return message, status.HTTP_400_BAD_REQUEST

    if email is None or email.strip == "" or not re.search(
            r'[\w.-]+@[\w.-]+.\w+', email):
        message = {"message": "ensure that email is not empty or filled out correctly"}
        return message, status.HTTP_400_BAD_REQUEST

    if password is None:
        message = {"message": "Password can not be empty"}
        return message, status.HTTP_400_BAD_REQUEST

    # Query to see if the user already exists
    user = Users.check_user(email)

    if not user:
        # There is no user so we'll try to register them
        try:
            # instantiate a user from the user class
            user = Users(first_name, last_name, email, password)
            # create new user and save them to the database
            user.save()

            message = {'message': "user has been created"}
            return message, status.HTTP_201_CREATED

        except Exception as error:
            # An error occured, therefore return a string message containing the error
            message = {'message':str(error)}

            return message, status.HTTP_401_UNAUTHORIZED
    else:
        # There is an existing user.
        # Return a message to the user telling them that they they already exist
        message = {'message': 'User already exists. Please login.'}

        return message, status.HTTP_202_ACCEPTED

        return message, status.HTTP_202_ACCEPTED


@app.route('/api/auth/login/', methods=['POST'])
def login():
    """Endpoint for loggig in users"""
    email = request.data.get('email')
    password = request.data.get('password')

    if email is None or password is None:
        message = {'message': 'inputs cannot be empty'}
        return message, status.HTTP_400_BAD_REQUEST

    try:
        # Get the user object using their email (unique to every user)
        user = Users.check_user(email)
        # Try to authenticate the found user using their password
        if user and user.verify_password(password):
            # Generate the access token. This will be used as the authorization header
            access_token = user.generate_token(user.id)
            if access_token:
                response = {
                    'message': 'You logged in successfully.',
                    'access_token': access_token.decode()
                }
            return response, status.HTTP_200_OK

        # else user does not exist. Return error message
        response = {
            'message': "Invalid Email or Password, Please Try again"
        }
        return response, status.HTTP_401_UNAUTHORIZED

    except Exception as error:
        # Create a response containing an string error message
        response = {
            'message': str(error)
        }
        return response, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/api/auth/logout/', methods=['POST'])
def logout():
    """User Logout endpoints logs out a user"""
    access_token = authentication_request()

    if access_token:
        # Attempt to decode the token and get the User ID
        user_id = Users.decode_token(access_token)
        if not isinstance(user_id, str):
            blacklist_token = BlackListToken(token=access_token)

            try:
                blacklist_token.logout()

                return {"message":"succesfully logged out"}, status.HTTP_200_OK

            except Exception as error:

                return {"message": str(error)}, status.HTTP_200_OK
        else:
            return {"message":user_id}, status.HTTP_401_UNAUTHORIZED

    return {"message": "Provide a valid authentication token"}, status.HTTP_403_FORBIDDEN


@app.route('/api/auth/reset-password/', methods=['POST'])
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
def events_list():
    """List or create events."""
    access_token = authentication_request()
    #page number used in pagination
    page = request.args.get('page', 1, type=int)

    if access_token:
        # Attempt to decode the token and get the User ID
        user_id = Users.decode_token(access_token)
        if not isinstance(user_id, str):
            # Go ahead and handle the request, the user is authenticated
            if request.method == 'POST':

                event = request.data.get('event')
                location = request.data.get('location')
                category = request.data.get('category')
                date = request.data.get('date')

                if event is None or location is None or date is None:
                    message = {'message': 'inputs cannot be empty, please fill all inputs'}
                    return message, status.HTTP_400_BAD_REQUEST

                if category is None:
                    category = "No category"
                else:
                    category = category

                inst = Events(event, location, category, date, created_by=user_id)
                inst.save()
                response = {
                    'id': inst.id,
                    'event': inst.event,
                    'location': inst.location,
                    'category': inst.category,
                    'date': inst.date
                }
                return response, status.HTTP_201_CREATED

            # Request.method == 'GET'
            # GET all the events created by this user
            events = Events.get_all_user_events(user_id, page)
            # events = Events.query.paginate(page, 5, error_out=True)
            results = []
            for event in events.items:
                obj = {
                    'id': event.id,
                    'event': event.event,
                    'location': event.location,
                    'category': event.category,
                    'date': event.date
                }
                results.append(obj)
            return results, status.HTTP_200_OK
        else:
            # user is not legit, so the payload is an error message
            message = user_id
            response = {
                'message': message
            }
            return response, status.HTTP_401_UNAUTHORIZED

    # request.method == 'GET'
    # GET all the events in the db
    events = Events.query.paginate(page, 5, error_out=True)
    results = []
    for event in events.items:
        obj = {
            'id': event.id,
            'event': event.event,
            'location': event.location,
            'category': event.category,
            'date': event.date
        }
        results.append(obj)
    return results, status.HTTP_200_OK


@app.route("/api/events/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def events_details(key):
    """Retrieve, update or delete events instances."""
    access_token = authentication_request()
    if access_token:
        # Get the user id related to this access token
        user_id = Users.decode_token(access_token)
        if not isinstance(user_id, str):
            # If the id is not a string(error), we have a user id
            # Retrieve Events by id
            get_event = Events.get_single_event(key)
            if not get_event:
                #if there is no event Rise Not found exception
                raise exceptions.NotFound()

            if request.method == 'PUT':
                event = request.data.get('event')
                location = request.data.get('location')
                category = request.data.get('category')
                date = request.data.get('date')

                if event is None or location is None or date is None:
                    return {'message': 'inputs cannot be empty, please fill all inputs'}

                get_event.event = event
                get_event.location = location
                get_event.date = date
                get_event.category = category
                #save the updated event
                get_event.save()
                response = {
                    'id': get_event.id,
                    'event': get_event.event,
                    'category': get_event.category,
                    'location': get_event.location,
                    'date': get_event.date,
                }
                return response, status.HTTP_201_CREATED

            elif request.method == "DELETE":
                get_event.delete()
                message = {"message": "Deleted succesfully"}
                return message, status.HTTP_204_NO_CONTENT

            # request.method == 'GET':
            response = {
                'id': get_event.id,
                'event': get_event.event,
                'location': get_event.location,
                'catogory': get_event.category,
                'date': get_event.date
            }
            return response, status.HTTP_200_OK
        else:
            # user is not legit, so the payload is an error message
            message = user_id
            response = {
                'message': message
            }
            # return an error response, telling the user he is Unauthorized
            return response, status.HTTP_401_UNAUTHORIZED
    get_event = Events.get_single_event(key)
    # request.method == 'GET':
    response = {
        'id': get_event.id,
        'event': get_event.event,
        'location': get_event.location,
        'catogory': get_event.category,
        'date': get_event.date
    }
    return response, status.HTTP_200_OK


@app.route("/api/events/<int:key>/rsvp/", methods=['GET', 'POST'])
def rsvp_event(key):
    """ Handles the RSVP logic"""
    access_token = authentication_request()

    if access_token:
        # Get the user id related to this access token
        user_id = Users.decode_token(access_token)

        if not isinstance(user_id, str):
            # If the id is not a string(error), we have a user id
            #Retrieve Events by id
            get_event = Events.get_single_event(key)

            if not get_event:
                #if there is no event Rise Not found exception
                raise exceptions.NotFound()

            if request.method == "POST":
                if not get_event.already_rsvpd(user_id):
                    get_event.rsvp_user(user_id)
                    return {
                        'message': "Thank you for registering to attend this event"
                        }, status.HTTP_201_CREATED
                return {"message":"You have already RSVP'd to this event"}, status.HTTP_202_ACCEPTED

            # request method GET
            rsvp_list = get_event.rsvp.all()
            return [users.get_full_names() for users in rsvp_list], status.HTTP_200_OK
        else:
            # user is not legit, so the payload is an error message
            message = user_id
            response = {
                'message': message
            }
            # return an error response, telling the user he is Unauthorized
            return response, status.HTTP_401_UNAUTHORIZED
    return {"message": "You need to sign in to RSVP"}, status.HTTP_403_FORBIDDEN
