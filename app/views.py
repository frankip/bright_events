# views.py
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

from app import app

events = {}
def api_view(key):
        return {
            'text': events[key],
            'url': request.host_url.rstrip('/') + url_for('events_details', key=key)
        }

@app.route("/api/events", methods=['GET', 'POST'])
def events_list():
    """
    List or create events.
    """
    if request.method == 'POST':
        name = str(request.data.get('text',''))
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
        name = str(request.data.get('text',''))
        events[key] = name
        return api_view(key)

    elif request.method == "DELETE":
        events.pop(key, None)
        return '', status.HTTP_204_NO_CONTENT

    if key not in events:
        raise exceptions.NotFound()
    return api_view(key)

          
