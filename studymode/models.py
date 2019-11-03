from studymode import db
from datetime import datetime

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    start_time = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    location = db.relationship('Location', backref = 'Place', lazy = True)
    class_name = db.Column(db.String, nullable = False)
