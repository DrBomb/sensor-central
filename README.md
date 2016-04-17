#Script for logging and displaying MQTT feeds

##Requires
* Flask
* Flask-SqlAlchemy
* paho-mqtt
* Gunicorn

##Configuration
This is a work in progress.

The idea is to have several modules or "Views" that have their behaviour defined inside their .py module definition. These views can have their own database table, html and javascript templates for functionality and REST endpoints for querying data.

Each view class must have:
* A constructor with the following parameters:
  * A name
  * A Title (For rendering in HTML)
  * A list of it's MQTT topics that are used for this view
  * The flask app object that will be bound to
* A flask blueprint object that will be registered in the route defined by the name assigned to the view
* A table object that must use the db object of flaks-sqlalchemy which will define the table on where the logged data will be stored
* A record method which will have a MQTT message as an argument and will parse the message and store on its respective database table

##Running
`pip install -r requirements.txt` to install dependencies

`python webapp.py` to use flask's internal webserver

`gunicorn webapp:app.app` to use gunicorn's WSGI server
