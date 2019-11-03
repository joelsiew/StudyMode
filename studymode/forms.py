from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.fields.html5 import DateTimeLocalField


class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField("Email",
                        validators=[DataRequired(), Email()])

    password = PasswordField("Password",
                             validators=[DataRequired()])

    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')


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
