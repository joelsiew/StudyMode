from studymode import app
from flask import url_for, render_template
from flask_googlemaps import Map, icons
from .forms import RegistrationForm, LoginForm, EventForm
import geocoder


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/map')
def draw_map():
    g = geocoder.ip('me')
    latitude, longitude = g.latlng[0], g.latlng[1]
    studymap = Map(
        identifier="study",
        varname="studymap",
        style="height:720px;width:1100px;margin:0;",  # hardcoded!
        lat=latitude,
        lng=longitude,
        zoom=15,
        markers=[]
    )
    return render_template('map.html', studymap=studymap)


@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title="Registration", form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title="Login", form=form)

