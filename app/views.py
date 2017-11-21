# views.py

from flask import request, url_for

from app import app


@app.route('/example/')
def example():
    return {'hello': 'world'}
