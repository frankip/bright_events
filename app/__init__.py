# app/__init__.py

# Third party imports
from flask_api import FlaskAPI, status, exceptions
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

# Initialize the app
app = FlaskAPI(__name__, instance_relative_config=True)
app.secret_key = "string"
app.config['SWAGGER'] = {
    'title': 'Bright Events'
}
db.init_app(app)
# Load the views
from app import views

# # Load the config file
app.config.from_object('config')

