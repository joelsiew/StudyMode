from studymode import app, db, bcrypt
from flask import url_for, render_template, redirect, flash
from studymode.map import draw_map
from studymode.forms import LoginForm, RegistrationForm
from studymode.models import User
from flask_login import login_user, current_user, logout_user, login_required, UserMixin


@app.route('/')
def home():
    people = User.query.all()
    return render_template('home.html', people=people)


@app.route('/map')
def map():
    studymap = draw_map()
    return render_template('map.html', studymap=studymap)


@app.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(password=form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)



@app.route('/login')
def login():
    return render_template('login.html')
