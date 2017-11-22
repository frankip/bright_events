# views.py
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

from app import app

events = {
    0: 'dev fest',
    1: 'andela bootcamp',
    2: 'for loop nairobi',
}
def note_repr(key):
        return {
            'text': events[key]
        }

@app.route("/api/events", methods=['GET', 'POST'])
def events_list():
    """
    List or create notes.
    """
    # request.method == 'GET'
    return [note_repr(idx) for idx in sorted(events.keys())]