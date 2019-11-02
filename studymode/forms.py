from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=10)])
    submit = SubmitField('Log In')

