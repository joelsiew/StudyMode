from studymode import app
from flask import url_for, render_template

@app.route('/')
def hello_world():
    return render_template('home.html')
