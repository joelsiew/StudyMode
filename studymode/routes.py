from studymode import app
from flask import url_for, render_template
import geocoder
from studymode.map import draw_map


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/map')
def map():
    studymap = draw_map()
    return render_template('map.html', studymap=studymap)


@app.route('/register')
def register():
    return render_template('register.html')



@app.route('/login')
def login():
    return render_template('login.html')
