[![Build Status](https://travis-ci.org/frankip/bright_events.svg?branch=v2_events)](https://travis-ci.org/frankip/bright_events)
[![Coverage Status](https://coveralls.io/repos/github/frankip/bright_events/badge.svg?branch=development)](https://coveralls.io/github/frankip/bright_events?branch=development)
[![Maintainability](https://api.codeclimate.com/v1/badges/f1998862ddd21c5fc013/maintainability)](https://codeclimate.com/github/frankip/bright_events/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f1998862ddd21c5fc013/test_coverage)](https://codeclimate.com/github/frankip/bright_events/test_coverage)
# Bright_events
Bright events provides a platform for event organizers to create and manage different types of events while making them easily accessible to target markets

## Requirements
    - python3
    - postgresSQL Databse Engine

## Links

- You can also view the [Designs Here](https://confident-colden-f872a4.netlify.com/sign-in.html)

- Link to Hosted [demo](https://eventsbright.herokuapp.com/api/events/)

- Access the API Documentation [Here](https://eventsbright.herokuapp.com/apidocs/#/)
# Installation  ##

1. Clone the Github repo to your machine 

     ``` git clone https://github.com/frankip/bright_events.git ```

2. change the directory to the project by 

    ``` cd bright_events ```

3. change to the active branch

    ``` git checkout development ```

4. Create a virtual enviroment

    ``` virtualenv -p python3 venv```
5. Activate the enviroment

    ``` source venv/bin/activate```

6. Install the project requirements

    ``` pip install -r requirements.txt ```

## **postgresSQl Set Up**
1. Intall Postgress

    - ```sudo apt-get install postgresql postgresql-contrib```

2. switch to postgress account

    - ```sudo -i -u postgres```

3. create database
    
        psql -c "CREATE DATABASE flask_api;" -U postgres
        psql -c "CREATE DATABASE test_db;" -U postgres

4. create user and set password

    - ```psql -c "CREATE USER test WITH PASSWORD 'admin';" -U postgres```

5. Run migrations

        python manage.py db init
        python manage.py db migrate
        python manage.py db upgrade

### set enviroment variables

on the terminal run

- ```export DATABASE_URL='postgresql://postgres:@localhost/flask_api'```

# Run 
To test our project on your terminal run 

``` export FLASK_APP=run.py```

then

``` flask run ```

on your browser open up [http://127.0.0.1:5000/api/events/](http://127.0.0.1:5000/api/events/)

# Testing using postman or curl 

the endpoints for the API are

        POST    /api/auth/register/
        POST    /api/auth/login/
        POST    /api/auth/logout/
        POST    /api/auth/reset-password/
        POST    /api/events/
        GET     /api/events/
        GET     /api/events/<int:key>/
        PUT     /api/events/<int:key>/
        POST    /api/events/<int:key>/rsvp
        GET    /api/events/<int:key>/rsvp

use the API documentation to get sample data of payload [Here](https://eventsbright.herokuapp.com/apidocs/#/)

do not forget to include the headers on your postman 
 - Content-Type: application/json
 - Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiO

make sure to register and login first to get the authorization token.
Copy the token and paste it into the header section, creating an Authorization header. Don't forget to put the word Bearer before the token with a space separating them like this:

```Bearer eyJ0eXATQsImV4cCI6ViIjo1fQ.8ju7doEn6Q8VJ6WXAnBHKlyn8KCkMr....```
## Test /api/auth/register/
    
    curl -H "Accept: application/json"\-H "Content-type: application/json" -X POST \
	-d '{"email": "test@test.com", "password": "test_password"}' \
	http://127.0.0.1:5000/api/auth/register/

## TEST /api/auth/login/
    
    curl -H "Accept: application/json" \
	-H "Content-type: application/json" -X POST \
	-d '{"email": "test@test.com", "password": "test_password"}' \
	http://127.0.0.1:5000/api/auth/login/
    