from flask import Flask
from flask_googlemaps import GoogleMaps, Map
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret
app.config['GOOGLEMAPS_KEY'] = config.api_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
GoogleMaps(app)
db = SQLAlchemy(app)
db.create_all()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from studymode import routes
