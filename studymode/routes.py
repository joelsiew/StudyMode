from studymode import app
from flask import url_for, render_template, flash, redirect
import geocoder
from studymode.map import draw_map
from .forms import RegistrationForm, LoginForm, EventForm

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/map')
def map():
    studymap = draw_map()
    return render_template('map.html', studymap=studymap)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Registration", form=form)




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'user@email.com' and form.password.data == 'password':
            flash("You have been logged in!", 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title="Login", form=form)