from flask import Flask
from flask.ext.googlemaps import GoogleMaps


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
GoogleMaps(app)

from studymode import routes

