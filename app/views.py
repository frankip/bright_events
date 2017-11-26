"""
this files contains the logic and the routes of the app
"""
from flask import request, url_for, abort
from flask_api import status, exceptions

from app import app
from . models import Users

events = {}
# Users = {}

@app.route('/api/auth/register', methods=['POST'])
def registration():
    """
    This function handles the user registration
    """
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        abort(400)
        
    inst = Users(username, password)
    inst.hash_password(password)
    inst.check_user(username)
    inst.save()

    # print(Users.user_db.keys())
    return "user created", status.HTTP_201_CREATED

@app.route('/api/auth/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        abort(400)

    if not Users.user_db.keys():
            abort(400)

    inst = Users(username, password)
    if username in Users.user_db.keys():
        if Users.user_db[username] == inst.verify_password(password):
            return "Logged in succesfully", status.HTTP_200_OK
        else:
            return "username/password incorrect", status.HTTP_401_UNAUTHORIZED

    return abort(400)

    # if Users.user_db[username] == inst.verify_password(password):
    #     return "logged in successfuly"
    # else:
    #     return "usernam/password is incorrect"
    # inst = Users(username, password)
    # Users.auth_verify_credentials(username, password, password)

def api_view(key):
    """
    Handles how the data will be 
    in the browsable api
    """
    return {
        'name': events[key],
        'url': request.host_url.rstrip('/') + url_for('events_details', key=key)
    }

@app.route("/api/events", methods=['GET', 'POST'])
def events_list():
    """
    List or create events.
    """
    if request.method == 'POST':
        name = str(request.data.get('text', ''))
        # if the dictonary is empty assign id manualy
        if not events.keys():
            ids_ = 0
        else:
            ids_ = max(events.keys())+1

        events[ids_] = name
        return api_view(ids_), status.HTTP_201_CREATED

    # request.method == 'GET'
    return [api_view(ids_) for ids_ in sorted(events.keys())]

@app.route("/api/events/<int:key>/", methods=['GET', 'PUT','DELETE'])
def events_details(key):
    """
    Retrieve, update or delete events instances.
    """
    if request.method == 'PUT':
        name = str(request.data.get('text', ''))
        events[key] = name
        return api_view(key)

    elif request.method == "DELETE":
        events.pop(key, None)
        return '', status.HTTP_204_NO_CONTENT

    if key not in events:
        raise exceptions.NotFound()
    return api_view(key)
