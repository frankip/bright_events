# app/__init__.py

# Third party imports
from flask import Flask

# local imports
from config import app_config

# Initialize the app
def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	# app.config.from_object(app_config[config_name])
	# app.config.from_pyfile('config.py')
	# init_app(app)

	# temporary route
	@app.route('/')
	def hello_world():
		return 'Hello, World!'

	return app


# # Load the views
# from app import views

# # Load the config file
# app.config.from_object('config')