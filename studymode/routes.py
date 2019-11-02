from studymode import app
from flask import url_for, render_template
from flask_googlemaps import Map, icons
from flask import url_for, render_template, redirect


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/map')
def draw_map():

    studymap = Map(
        identifier="study",
        varname="studymap",
        style="height:720px;width:1100px;margin:0;",  # hardcoded!
        lat=37.4419,  # hardcoded!
        lng=-122.1419,  # hardcoded!
        zoom=15,
        markers=[(37.4419, -122.1419)]
    )
    return render_template('map.html', studymap=studymap)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')
