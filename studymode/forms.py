from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField("Email",
                        validators=[DataRequired(), Length(min=2, max=120)])

    password = PasswordField("Password",
                             validators=[DataRequired()])

    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email',
                           validators=[DataRequired(), Length(min=2, max=120)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=2, max=20)])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class EventForm(FlaskForm):
    course = StringField('Course',
                         validators=[DataRequired(), Length(min=1)])
    address = StringField('Address',)

    locked = BooleanField('Private Event', )

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')
