from studymode import db
from datetime import datetime

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    start_time = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    location = db.relationship('Location', backref = 'Place', lazy = True)
    class_name = db.Column(db.String, nullable = False)
    private_event = db.Column(db.Boolean, nullable = False, default = False)
    private_password = db.Column(db.String(20), default='password')
    event_name = db.Column(db.String(20), nullable = False, default='Study session')
