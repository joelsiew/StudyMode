import collections

from studymode import app, db, bcrypt
from flask import url_for, render_template, flash, redirect, request
from studymode.map import draw_map
from studymode.forms import (LoginForm, RegistrationForm, EventForm, ResetEmailForm,
                             ResetPasswordForm, ResetUsernameForm)
from studymode.models import User, Event
from flask_login import login_user, current_user, logout_user, login_required, UserMixin
import geocoder
import requests
import json


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('map'))
    else:
        return render_template('home.html', title='Home')


@app.route('/map')
@login_required
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
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/event', methods=['GET', 'POST'])
@login_required
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        g = geocoder.ip('me')
        current_latitude, current_longitude = g.latlng[0], g.latlng[1]
        response = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json?latlng=30.282998,-97.738470&key=AIzaSyBq_qn6etPVIO8OZVTvPHtk7JMCriN04wQ")
        json_data = json.loads(response.text)
        addy = json_data['results'][0]['formatted_address']
        temp_start = form.start_time_input.data.strftime('%Y-%m-%dT%H:%M')
        temp_end = form.end_time_input.data.strftime('%Y-%m-%dT%H:%M')
        event = Event(latitude=current_latitude, longitude=current_longitude, class_name=form.course.data,
                      user_id=current_user.id, start_time=temp_start, end_time=temp_end, address=addy)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('map'))
    return render_template('add_event.html', title="Add Event", form=form)


@app.route('/events')
@login_required
def events():
    events = Event.query.all()
    date = collections.deque()
    for x in events:
        date.appendleft("{}-{}-{}".format(x.start_time[5:7], x.start_time[8:10], x.start_time[0:4]))

        x.start_time = "{}".format(x.start_time[12:16])
        x.end_time = "to {}".format(x.end_time[12:16])

    return render_template('events.html', title='Events', events=events, date=date)

@app.route('/account_settings')
@login_required
def account_settings():
    return render_template('account_settings.html', title='Account Settings')

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/reset_password", methods=['GET','POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        temp = form.password.data.encode('utf-8')
        hashed_pw = bcrypt.generate_password_hash(password=temp).decode('utf-8')
        current_user.password = hashed_pw
        db.session.commit()
        flash('Your password has been updated! You can now log in.', 'success')
        return redirect(url_for('map'))
    return render_template('reset_account.html', title='Reset Acount Info', form=form)

@app.route("/reset_username", methods=['GET','POST'])
def reset_username():
    form = ResetUsernameForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Your username has been updated! You can now log in.', 'success')
        return redirect(url_for('map'))
    user = User.query.filter_by(username=form.username.data).first()
    return render_template('reset_username.html', title='Reset Username', form=form)

@app.route("/reset_email", methods=['GET','POST'])
def reset_email():
    form = ResetEmailForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        flash('Your email has been updated! You can now log in.', 'success')
        return redirect(url_for('map'))
    return render_template('reset_email.html', title='Reset Email', form=form)



