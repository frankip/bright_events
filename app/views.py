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
    if key:
        return {
            'url': request.host_url.rstrip('/') + url_for('events', key=key),
            'text': events[key]
        }


@app.route("/api/events", methods=['GET', 'POST'])
def events_list():
    """
    List or create notes.
    """
    if request.method == 'POST':
        event_name = str(request.data.get('text', ''))
        idx = max(events.keys()) + 1
        events[idx] = event_name
        return note_repr(idx), status.HTTP_201_CREATED

    elif max(events.keys())<0:
        return {"sorry no events at the moment"}
    # request.method == 'GET'
    return [note_repr(idx) for idx in sorted(events.keys())]