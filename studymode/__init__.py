from flask import Flask
from flask_googlemaps import GoogleMaps, Map
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDXtCfWA1EuXPc4geNQTm2NsIb8xllcCac"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
GoogleMaps(app)
db = SQLAlchemy(app)
db.create_all()
bcrypt = Bcrypt(app)

from studymode import routes

