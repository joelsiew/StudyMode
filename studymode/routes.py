import collections

from studymode import app, db, bcrypt
from flask import url_for, render_template, flash, redirect, request, abort
from studymode.map import draw_map
from studymode.forms import LoginForm, RegistrationForm, EventForm, UpdateAccountForm
from studymode.models import User, Event
from flask_login import login_user, current_user, logout_user, login_required, UserMixin
import geocoder
import requests
import json
import pytz
from tzlocal import get_localzone
from datetime import datetime, timezone

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


def get_dt(yr, mo, day, hr, min):
    dt = str()
    h = 12 if hr % 12 == 0 else hr
    dt += str(yr) + '-' + str(mo) + '-' + str(day)
    dt += 'T' + str(h) + ':' + str(min)
    dt_obj = datetime.strptime(dt, '%Y-%m-%dT%H:%M')
    return dt_obj


@app.route('/event', methods=['GET', 'POST'])
@login_required
def add_event():
    form = EventForm()
    if request.method == 'GET':
        x = datetime.now()
        dt_obj = get_dt(x.year, x.month, x.day, x.hour, x.minute)
        form.start_time_input.data = dt_obj
        form.end_time_input.data = dt_obj

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

@app.route("/update_account_info", methods=['GET','POST'])
def update_account_info():
    form = UpdateAccountForm()
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    if form.validate_on_submit():
        temp = form.password.data.encode('utf-8')
        hashed_pw = bcrypt.generate_password_hash(password=temp).decode('utf-8')
        current_user.password = hashed_pw
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated! You can now log in.', 'success')
        return redirect(url_for('map'))
    return render_template('update_account_info.html', title='Update Account Info', form=form)


@app.route("/delete_event<event_id>", methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author != current_user:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('Your event has been deleted!', 'success')
    return redirect(url_for('home'))

