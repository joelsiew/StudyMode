from flask_login import UserMixin
from studymode import db, login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    events = db.relationship('Event', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.id}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    start_time = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    longitude = db.Column(db.Float(precision=2), nullable=False)
    latitude = db.Column(db.Float(precision=2), nullable=False)
    class_name = db.Column(db.String, nullable = False)
    private_event = db.Column(db.Boolean, nullable = False, default = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Event('{self.class_name}', '{self.latitude}', '{self.longitude}')"


