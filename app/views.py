"""
this files contains the logic and the routes of the app
"""
from flask import request, url_for, abort, g, jsonify, session
from flask_api import status, exceptions

from app import app
from . models import Users, Events

# events = {}
# Users = {}

@app.route('/api/auth/register', methods=['POST'])
def registration():
    """
    This function handles the user registration
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        abort(400)
    user = Users(username, password)
    if username in Users.user_db.keys():
            return "User already exists. Please login.", status.HTTP_202_ACCEPTED
    cur_user = user.save()

    return {'username': cur_user.username}, status.HTTP_201_CREATED

@app.route('/api/auth/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')


    if username is None or password is None:
        abort(400)

    if not Users.user_db.keys():
            abort(400)

    user = Users(username, password)
    if username in Users.user_db.keys():
        if Users.user_db[username] == password:
            g.user = user
            session['user'] = g.user.username
            return {'logged in': g.user.username}, status.HTTP_200_OK
        else:
            return "username/password incorrect", status.HTTP_401_UNAUTHORIZED

    return "username/password incorrect", status.HTTP_401_UNAUTHORIZED

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    if 'user' not in session:
        return "you have to login first"
    else:
        session.pop('user')
        return "you have been logged out"

# app.route('/api/auth/reset-password', methods=['POST'])
# def reset_password():

@app.route('/api/token')
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})

def api_view(key):
    """
    Handles how the data will be 
    in the browsable api
    """
    return {
        'name': Events.events_db[key],
        'url': request.host_url.rstrip('/') + url_for('events_details', key=key)
    }

@app.route("/api/events", methods=['GET', 'POST'])
def events_list():
    """
    List or create events.
    """
    if request.method == 'POST':
        name = request.json.get('text', '')
        location = request.json.get('location', '')
        date = request.json.get('date', '')
        inst = Events(name, location, date)
        ids_= inst.add_event()
        return api_view(ids_), status.HTTP_201_CREATED

    # request.method == 'GET'
    return [api_view(ids_) for ids_ in sorted(Events.events_db.keys())]

@app.route("/api/events/<int:key>/", methods=['GET', 'PUT','DELETE'])
def events_details(key):
    """
    Retrieve, update or delete events instances.
    """
    if request.method == 'PUT':
        name = str(request.data.get('text', ''))
        Events.events_db[key] = name
        return api_view(key)

    elif request.method == "DELETE":
        Events.events_db.pop(key, None)
        return '', status.HTTP_204_NO_CONTENT

    if key not in Events.events_db:
        raise exceptions.NotFound()
    return api_view(key)
