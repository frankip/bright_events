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

