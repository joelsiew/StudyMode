from studymode import app
from flask import render_template
from studymode.forms import LoginForm


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')
