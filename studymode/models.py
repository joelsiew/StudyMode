from studymode import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    events = db.relationship('Event', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    start_time = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    location = db.relationship('Location', backref = 'Place', lazy = True)
    class_name = db.Column(db.String, nullable = False)
    private_event = db.Column(db.Boolean, nullable = False, default = False)
    private_password = db.Column()


class Location(db.Model):
    longitude = db.Column(db.Float(min=-180, max=180, nullable=False))
    latitude = db.Column(db.Float(min=-90, max=90), nullable=False)
    address = db.Column(db.String, nullable=False)
    zipcode = db.Column(db.Integer(min=00000, max=99999), nullable=False)