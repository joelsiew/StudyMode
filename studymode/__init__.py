from flask import Flask
from flask_googlemaps import GoogleMaps, Map

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDXtCfWA1EuXPc4geNQTm2NsIb8xllcCac"
GoogleMaps(app)

from studymode import routes

