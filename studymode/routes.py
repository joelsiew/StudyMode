from studymode import app, db, bcrypt
from flask import url_for, render_template, flash, redirect
import geocoder
from studymode.map import draw_map
from studymode.models import User
from .forms import RegistrationForm, LoginForm, EventForm

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/map')
def map():
    studymap = draw_map()
    return render_template('map.html', studymap=studymap)


@app.route('/register')
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Registration", form=form)




@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title="Login", form=form)
