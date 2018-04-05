# app/__init__.py
import os
# Third party imports
from flask_api import FlaskAPI, status, exceptions
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

# Initialize the app
app = FlaskAPI(__name__, instance_relative_config=True)
# Load the config file
app.config.from_object(app_config['development'])
app.secret_key = os.getenv('SECRET')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.url_map.strict_slashes = False
app.config['SWAGGER'] = {
    'title': 'Bright Events'
}
db.init_app(app)

# Load the views
from app import views
