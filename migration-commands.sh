#!/bin/bash

#migration commands
python manage.py db init
python manage.py db migrate
python manage.py db upgrade