# views.py
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

from app import app

events = {}
def api_view(key):
        return {
            'text': events[key]
        }

@app.route("/api/events", methods=['GET', 'POST'])
def events_list():
    """
    List or create notes.
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
