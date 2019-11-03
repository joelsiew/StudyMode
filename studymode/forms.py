from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from wtforms.fields.html5 import DateTimeLocalField
from wtforms_components import TimeField
from studymode.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already taken')


class LoginForm(FlaskForm):
    email = StringField('Email',
                           validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=2, max=20)])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class EventForm(FlaskForm):
    course = StringField('Course', validators=[DataRequired(), Length(min=1)])
    start_time_input = DateTimeLocalField('Enter Start Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_time_input = DateTimeLocalField('Enter End Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password",
                             validators=[DataRequired()])

    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Reset Password')

class ResetUsernameForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=20)])

    submit = SubmitField('Reset Username')

class ResetEmailForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])

    submit = SubmitField('Reset Email')