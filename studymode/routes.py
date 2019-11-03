from studymode import app, db, bcrypt
from flask import url_for, render_template, flash, redirect, request
from studymode.map import draw_map
from studymode.forms import LoginForm, RegistrationForm, EventForm
from studymode.models import User, Event
from flask_login import login_user, current_user, logout_user, login_required, UserMixin


@app.route('/')
def home():
    people = User.query.all()
    return render_template('home.html', people=people)


@app.route('/map')
def map():
    events = Event.query.all()
    studymap = draw_map()
    return render_template('map.html', studymap=studymap)


@app.route('/register', methods=['GET', 'POST'])
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('try again fam', 'danger')
    return render_template('login.html', title='Log In', form=form)

@app.route('/add_event')
def add_event():
    form = EventForm()
    return render_template('add_event.html', title="Add Event", form=form)

@app.route('/events')
def events():
    #events = Event.query.all()
    test_events = [
        {
            'start_time': '8:00',
            'end_time': '10:00',
            'class_name': 'EE302'
        },
        {
            'start_time': '10:00',
            'end_time': '12:00',
            'class_name': 'EE411'
        },
        {
            'start_time': '12:00',
            'end_time': '2:00',
            'class_name': 'EE427J'
        }
    ]
    return render_template('events.html', title='Events', test_events=test_events)
