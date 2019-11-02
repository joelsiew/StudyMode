from studymode import app
from flask import url_for, render_template

@app.route('/')
def hello_world():
    return render_template('home.html')
@app.route('/map')
def draw_map():
    return render_template('map.html')
