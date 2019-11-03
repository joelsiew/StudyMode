from studymode import app, db, bcrypt
from flask import url_for, render_template, flash, redirect, request
from studymode.map import draw_map
from studymode.forms import (LoginForm, RegistrationForm, EventForm, ResetEmailForm,
                             ResetPasswordForm, ResetUsernameForm)
from studymode.models import User, Event
from flask_login import login_user, current_user, logout_user, login_required, UserMixin
import geocoder


@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', title='Home')
    else:
        return redirect(url_for('register'))


@app.route('/map')
def map():
    events = Event.query.all()
    studymap = draw_map(events)
    return render_template('map.html', studymap=studymap)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        temp = form.password.data.encode('utf-8')
        hashed_pw = bcrypt.generate_password_hash(password=temp).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('try again fam', 'danger')
    return render_template('login.html', title='Log In', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/event',methods=['GET', 'POST'])
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        g = geocoder.ip('me')
        current_latitude, current_longitude = g.latlng[0], g.latlng[1]
        event = Event(start_time=form.start_time, end_time=form.end_time, latitude=current_latitude,
                      longitude=current_longitude, course=form.course.data, user_id=current_user.id)

    return render_template('add_event.html', title="Add Event", form=form)

@app.route('/events')
def events():
    events = Event.query.all()
    return render_template('events.html', title='Events', events=events)

@app.route('/account_settings', methods=['GET', 'POST'])
def account_settings():
    return render_template('account_settings.html', title='Account Settings')

@app.route('/account')
def account():
    return render_template('account.html', title='Account')

@app.route("/reset_password", methods=['GET','POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        temp = form.password.data.encode('utf-8')
        hashed_pw = bcrypt.generate_password_hash(password=temp).decode('utf-8')
        User.password = hashed_pw
        db.session.commit()
        flash('Your password has been updated! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)

@app.route("/reset_username", methods=['GET','POST'])
def reset_username():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetUsernameForm()
    if form.validate_on_submit():
        User.username = form.username.data()
        db.session.commit()
        flash('Your username has been updated! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_username.html', title='Reset Username', form=form)

@app.route("/reset_email", methods=['GET','POST'])
def reset_email():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetEmailForm()
    if form.validate_on_submit():
        User.email = form.email.data()
        db.session.commit()
        flash('Your email has been updated! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_email.html', title='Reset Email', form=form)
