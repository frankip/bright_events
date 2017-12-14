[![Build Status](https://travis-ci.org/frankip/bright_events.svg?branch=v2_events)](https://travis-ci.org/frankip/bright_events)
[![Coverage Status](https://coveralls.io/repos/github/frankip/bright_events/badge.svg?branch=v2_events)](https://coveralls.io/github/frankip/bright_events?branch=v2_events)
[![Maintainability](https://api.codeclimate.com/v1/badges/f1998862ddd21c5fc013/maintainability)](https://codeclimate.com/github/frankip/bright_events/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f1998862ddd21c5fc013/test_coverage)](https://codeclimate.com/github/frankip/bright_events/test_coverage)
# Bright_events
Bright events provides a platform for event organizers to create and manage different types of events while making them easily accessible to target markets

## Designs ##
* The Designs folder contains the static pages showing how the app will look like when finished
* It also contains the uml-class and wireframes of the respective pages

You can also view the [Designs Here](https://confident-colden-f872a4.netlify.com/sign-in.html)

### Wireframes 
![Alt sign-up](https://github.com/frankip/bright_events/blob/master/designs/wireframes/registration%20page.jpeg)
![Alt sign-in](https://github.com/frankip/bright_events/blob/master/designs/wireframes/login%20page.jpeg)
![Alt homepage](https://github.com/frankip/bright_events/blob/master/designs/wireframes/index.html.jpeg)
![Alt event details](https://github.com/frankip/bright_events/blob/master/designs/wireframes/details%20page.jpeg)

### uml-class diagram ###
![Alt Uml-diagram](https://github.com/frankip/bright_events/blob/master/designs/wireframes/uml.jpeg)

# Link to Hosted [demo](https://eventsbright.herokuapp.com/api/events/)
# Access the API Documentation [Here](https://eventsbright.herokuapp.com/apidocs/#/)
## To run the API  ##
first clone this repo to your machine 

 ``` git clone https://github.com/frankip/bright_events.git ```

then change the directory to the project by 

``` cd bright_events ```

to make sure all the packages needed to run the project present in your machine,
we'll create a virtual enviroment and install the packages there

* to create a virtual enviroment run


    ``` virtualenv -p python3 venv```
* activating the enviroment

    ``` source venv/bin/activate```

our virtual enviroment is now ready, we should install all packages for our project
ensure you have pip installed otherwise 


``` sudo apt install pip```

then on your terminal run

``` pip install -r requirements.txt ```

# run 
To test our project on your terminal run 

``` export FLASK_APP=run.py```

then

``` flask run ```

on your browser open up [http://127.0.0.1:5000/api/events/](http://127.0.0.1:5000/api/events/)

# Testing using postman or curl 

the endpoints for the api are

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

## Test /api/auth/register/
    
    curl -H "Accept: application/json"\-H "Content-type: application/json" -X POST \
	-d '{"email": "test@test.com", "password": "test_password"}' \
	http://127.0.0.1:5000/api/auth/register/

## TEST /api/auth/login/
    
    curl -H "Accept: application/json" \
	-H "Content-type: application/json" -X POST \
	-d '{"email": "test@test.com", "password": "test_password"}' \
	http://127.0.0.1:5000/api/auth/login/

## Test /api/events/

    
    curl -H "Accept: application/json" \
	-H "Content-type: application/json" -X POST \
	-d '{"title": "Fruits"}' \
	http://127.0.0.1:5000/api/events/
