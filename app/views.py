"""
this files contains the logic and the routes of the app
"""
from flask import request
from flask_api import status, exceptions

#local imports
from app import app
from .auth import (
    registration,
    login,
    logout,
    reset_password
)
from .models import (
    Events,
    Users
)
from .error import (
    not_found_error,
    internal_error,
    method_not_allowed
)

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

@app.route("/api/events/", methods=['GET', 'POST'])
def events_list():
    """create and list events"""

    # Get the access token
    access_token = authentication_request()
    #page number variable to used in pagination
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)

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
        
                if event is None or event.strip() == "":
                    message = {'message': 'event input field cannot be missing or empty'}
                    return message, status.HTTP_400_BAD_REQUEST
                
                if location is None or location.strip() == "":
                    message = {'message': 'location input field cannot be missing or empty'}
                    return message, status.HTTP_400_BAD_REQUEST
                
                if date is None or date.strip() == "":
                    message = {'message': 'date input field cannot be missing or empty'}
                    return message, status.HTTP_400_BAD_REQUEST
                
                # check if category is empty then put a default value
                if category is None or category.strip() == "":
                    category = "No Category"
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
    all_events = Events.query.paginate(page, limit, error_out=True)
    results = []
    for event in all_events.items:
        obj = {
            'id': event.id,
            'event': event.event,
            'location': event.location,
            'category': event.category,
            'date': event.date
        }
        results.append(obj)
    return results, status.HTTP_200_OK


@app.route("/api/events/search/", methods=['GET', 'POST'])
def filter_or_search_events():
    """Search or Filter the events list"""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 5, type=int)

    category = request.args.get('category')
    location = request.args.get('location')
    search  = request.args.get('q')
    if category and location:
        filterd = Events.query.filter_by(
            category=category, location=location).paginate(page, limit)

    elif category:
        filterd = Events.query.filter_by(
            category=category).paginate(page, limit)

    elif location:
        filterd = Events.query.filter_by(
            location=location).paginate(page, limit)

    elif search:
        filterd = Events.query.filter(
            getattr(Events, 'event').ilike('%{}%'.format(search))).paginate(page, limit)


    else:
        return {'message': 'That query can not be found'}

    response = []
    for results in filterd.items:
        obj = {
            'id': results.id,
            'event': results.event,
            'location': results.location,
            'category': results.category,
            'date': results.date
        }
        response.append(obj)

    # If there are no values in response return message
    if not response:
        return {'message': 'There are no events matching that query'}, status.HTTP_200_OK

    return response, status.HTTP_200_OK
    
    
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
            get_my_event = Events.get_single_event(key)
            if not get_my_event:
                #if there is no event Rise Not found exception
                raise exceptions.NotFound()

            if request.method == 'PUT':
                event = request.data.get('event')
                location = request.data.get('location')
                category = request.data.get('category')
                date = request.data.get('date')

                if event is None or location is None or date is None:
                    return {'message': 'inputs cannot be empty, please fill all inputs'}

                get_my_event.event = event
                get_my_event.location = location
                get_my_event.date = date
                get_my_event.category = category
                #save the updated event
                get_my_event.save()
                response = {
                    'id': get_my_event.id,
                    'event': get_my_event.event,
                    'category': get_my_event.category,
                    'location': get_my_event.location,
                    'date': get_my_event.date,
                }
                return response, status.HTTP_201_CREATED

            elif request.method == "DELETE":
                get_my_event.delete()
                message = {"message": "Deleted succesfully"}
                return message, status.HTTP_204_NO_CONTENT

            # request.method == 'GET':
            response = {
                'id': get_my_event.id,
                'event': get_my_event.event,
                'location': get_my_event.location,
                'category': get_my_event.category,
                'date': get_my_event.date
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

    # Un registerd usercan still view the event
    # request.method == 'GET':
    get_event = Events.get_single_event(key)
    if not get_event:
        #if there is no event Rise Not found exception
        raise exceptions.NotFound()
        
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
