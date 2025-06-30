
#  Event Planner — Backend API

A RESTful Flask API built to manage events and reviews for the Event Planner frontend.
Authenticated users can post new events and submit reviews after signing in.
SQLite used for persistence and deployed on Railway.

##  Live API Endpoint

 [API Base URL](https://event-planner-backend-production.up.railway.app)

##  Built With

- Flask + Flask-RESTful
- Flask-JWT-Extended (auth)
- SQLAlchemy + SQLite
- Flask-CORS
- Flask-Bcrypt
- Flask-Migrate

##  Features

- User registration and login
- View all public events in the homepage
- Submit new events and view detailed event info(authenticated)
- Submit and view reviews for events
- Filter by categories
- Lightweight SQLite backend

## API Endpoints

# Auth

Method	Endpoint	Description

POST	/signup	Register a new user
POST	/login	Log in and get token


# Events

Method	Endpoint	Description

GET	/events	Get all events
GET	/events/<id>	Get details for one event
POST	/events	Create a new event


# Reviews

Method	Endpoint	Description

GET	/events/<id>/reviews	Get all reviews for event
POST	/events/<id>/reviews	Add a new review to event



---

# Validation & Rules

User email must be unique

Event title and date are required

Review content must not be empty

Only logged-in users can post reviews or create events



---
# Notes


The app uses token-based auth 

Add CORS support for frontend-backend connection

[Watch video demo](https://drive.google.com/file/d/1vZgetG51WejjvCWi18dIElKR6GgxZw3G/view?usp=sharing)

## Contributors
  -Jeff Mbithi
  -Brian Bett
  -Bildad Ereggae
  -Maureen Nkirote
  -Carol Kosgei

##  Local Setup

git clone https://github.com/your-user/event-planner-backend
cd event-planner-backend
pipenv install packages
flask run
