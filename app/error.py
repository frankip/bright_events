from app import app, db
from flask_api import status


@app.errorhandler(404)
def not_found_error(error):
    response = {
        'message': 'The page you are looking for is not available'
    }
    return response, status.HTTP_404_NOT_FOUND


@app.errorhandler(500)
def internal_error(error):
    response = {
        'message': 'Un expected error has occured'
    }
    return response, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.errorhandler(405)
def method_not_allowed(error):
    response = {
        'message': 'That operation is not allowed'
    }
    return response, status.HTTP_405_METHOD_NOT_ALLOWED
