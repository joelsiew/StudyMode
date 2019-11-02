from studymode import db
from datetime import datetime
from flask_sqlalchemy import SQLa

class Location(db.Model):
    longitude = db.Column(db.Float(min = -180, max = 180), nullable = False)
    latitude = db.Column(db.Float(min =  -85.05112878, max = 85.05112878), nullable = False)
    address = db.Column(db.String(), nullable = False)
    zipcode = db.Column(db.Integer(min = 00501, max = 99950), nullable = False)
