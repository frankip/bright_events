# app/__init__.py

# Third party imports
from flask_api import FlaskAPI, status, exceptions

# local imports
from config import app_config

# Initialize the app
app = FlaskAPI(__name__, instance_relative_config=True)
app.secret_key = "string"

# Load the views
from app import views

# # Load the config file
app.config.from_object('config')
