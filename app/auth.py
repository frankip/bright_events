"""
this files contains the logic and the routes of the app
"""
import re
from flask import request, session
from flask_api import status, exceptions

#local imports
from app import app, db
from .models import Users, BlackListToken
from .password import is_strong_password


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

def check_password_validation(password):
    if password is None or not is_strong_password(password):
        message = {
            "message": "Password field can not be empty and it should contain an Uppercase, a lowercase, a digit and shoud be more than six characters"}
        return message, status.HTTP_400_BAD_REQUEST

    return password

@app.route('/api/auth/register/', methods=['GET', 'POST'])
def registration():
    """
    user registration endpoint registers a user and
    takes in a first name, last name, email, and password
    """
    # Retrieve data from the user side
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    password = request.data.get('password')

    """
    validating the data from user isalpha ensures there are no
    non-alphabet characters
    """

    if first_name is None or first_name.strip() == "" or not first_name.isalpha():
        message = {
            "message": "ensure the first name field is not empty and it consist of alphabets only"}
        return message, status.HTTP_400_BAD_REQUEST

    if last_name is None or last_name.strip() == "" or not last_name.isalpha():
        message = {
            "message": "ensure the last name field is not empty and it consist of alphabets only"}
        return message, status.HTTP_400_BAD_REQUEST

    if email is None or email.strip == "" or not re.search(
            r'[\w.-]+@[\w.-]+.\w+', email):
        message = {
            "message": "ensure that email field is not empty or is filled out correctly"}
        return message, status.HTTP_400_BAD_REQUEST

    valid_password = check_password_validation(password)
    
    # Query to see if the user already exists
    user = Users.check_user(email)

    if not user:
        # There is no user so we'll try to register them
        try:
            # hash password
            password = Users.hash_password(valid_password)
            # instantiate a user from the user class
            user = Users(first_name, last_name, email, password)
            # create new user and save them to the database
            user.save()

            message = {'message': "user has been created"}
            return message, status.HTTP_201_CREATED

        except Exception as error:
            # An error occured, therefore return a string message containing the error
            message = {'message': str(error)}

            return message, status.HTTP_401_UNAUTHORIZED
    else:
        # There is an existing user.
        # Return a message to the user telling them that they they already exist
        message = {'message': 'User already exists. Please login.'}

        return message, status.HTTP_202_ACCEPTED


@app.route('/api/auth/login/', methods=['POST'])
def login():
    """Endpoint for loggig in users"""
    email = request.data.get('email')
    password = request.data.get('password')

    if email is None or password is None:
        message = {'message': 'ensure that email field or password field is present'}
        return message, status.HTTP_400_BAD_REQUEST

    try:
        # Get the user object using their email (unique to every user)
        user = Users.check_user(email)
        # Try to authenticate the found user using their password
        if user and user.verify_password(password):
            # Generate the access token. This will be used as the authorization header
            access_token = user.generate_token(user.id)
            if access_token:
                response = {
                    'message': 'You logged in successfully.',
                    'access_token': access_token.decode()
                }
            return response, status.HTTP_200_OK

        # else user does not exist. Return error message
        response = {'message': 'Invalid Email or Password, Please Try again'}
        return response, status.HTTP_401_UNAUTHORIZED

    except Exception as error:
        # Create a response containing an string error message
        response = {
            'message': str(error)
        }
        return response, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/api/auth/logout/', methods=['POST'])
def logout():
    """User Logout endpoints logs out a user"""
    access_token = authentication_request()

    if access_token:
        # Attempt to decode the token and get the User ID
        user_id = Users.decode_token(access_token)
        if not isinstance(user_id, str):
            blacklist_token = BlackListToken(token=access_token)

            try:
                blacklist_token.logout()

                return {"message": "succesfully logged out"}, status.HTTP_200_OK

            except Exception as error:

                return {"message": str(error)}, status.HTTP_200_OK
        else:
            return {"message": user_id}, status.HTTP_401_UNAUTHORIZED

    return {"message": "Provide a valid authentication token"}, status.HTTP_403_FORBIDDEN


@app.route('/api/auth/reset-password/', methods=['PUT'])
def reset_password():
    """Reset user Password endpoint takes in a password and resets the password"""
    password = request.data.get('password')
    access_token = authentication_request()

    if access_token:
        # Attempt to decode the token and get the User ID
        user_id = Users.decode_token(access_token)
        if not isinstance(user_id, str):
            user = Users.query.filter_by(id=user_id).first()
            try:
                if not user:
                    raise exceptions.NotFound()

                valid_password = check_password_validation(password)
                user.password = Users.hash_password(valid_password)
                user.save()
                # db.session.commit()
                return {"message": "you have succesfuly reset your password"}, status.HTTP_200_OK
            
            except Exception as error:
                
                return {"message": str(error)}, status.HTTP_200_OK
                
        else:
            return {"message": user_id}, status.HTTP_401_UNAUTHORIZED

    return {"message": "Provide a valid authentication token"}, status.HTTP_403_FORBIDDEN
