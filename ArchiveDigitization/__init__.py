"""
ArchiveDigitization

Base python file for ArchiveDigitization Flask App

Copyright Joan Chirinos, 2021.
"""

import sys
import os
import uuid
import base64
# import datetime

from flask import (Flask, render_template, redirect, url_for, session, request,
                   flash, current_app)
from markupsafe import Markup

from util import db, helpers
import config

app = Flask(__name__)

# Production Config
app.config.from_object(config.ProdConfig)

# Development Config
# app.config.from_object(config.DevConfig)

# Database Manager with correct databse path and table defns path
with app.app_context():
    cwd = os.getcwd()
    dbm = db.DBManager(current_app.config['DATABASE_URI'],
                       f'{cwd}/static/table_definitions.sql')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    '''
    Catch-all route in case some typo happens or something
    '''
    flash(f'Invalid endpoint: /{path}', 'warning')
    return redirect(url_for('home'))


@app.route('/')
def home():
    '''
    Render the homepage.

    If user is logged in, redirect to their files.
    '''
    return render_template('index.html')


@app.route('/login')
def login_page():
    '''
    Render the login page.

    If user is logged in, redirect to home.
    '''
    if 'email' in session:
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/register')
def register_page():
    '''
    Render the registration page.

    If user is logged in, redirect to home.
    '''
    if 'email' in session:
        return redirect(url_for('home'))
    return render_template('register.html')


@app.route('/authenticate', methods=['POST'])
def authenticate():
    '''
    Attempt to log user in.

    On failure, flashes error and redirects home.
    On success, stores email in session and redirects to project page.
    '''
    email = request.form['email'].strip()
    password = request.form['password'].strip()

    if helpers.verify_auth_args(email, password)\
       and dbm.authenticate_user(email, password):
        session['email'] = email
        return redirect(url_for('home'))
    else:
        flash('Incorrect username or password!', 'danger')
        return redirect(url_for('home'))


@app.route('/registerUser', methods=['POST'])
def register():
    '''
    Attempt to register user.

    On failure, flashes error and redirects home.
    On success, stores email in session and redirects to home.
    '''
    first = request.form['first'].strip()
    last = request.form['last'].strip()
    email = request.form['email'].strip()
    password = request.form['password'].strip()

    if not helpers.verify_auth_args(first, last, email, password):
        flash('One or more fields is improperly formatted!', 'danger')
        return redirect(url_for('register_page'))
    elif not dbm.register_user(email, password, first, last):
        s = ('Email already in use! <a href="/login" class="alert-link">'
             + 'Log in?</a>')
        flash(Markup(s), 'danger')
        return redirect(url_for('home'))
    else:
        session['email'] = email
        flash('Account creastion successful!', 'success')
        return redirect(url_for('home'))


@app.route('/logout')
def logout():
    '''
    Attempt to log user out.

    Regardless, will redirect to home page.
    '''
    if 'email' in session:
        session.pop('email')
    return redirect(url_for('home'))


@app.route('/digitize')
def digitize_page():
    # if 'email' not in session:
    #     flash('You don\'t have access to that page!')
    #     return redirect(url_for(home))
    return render_template('digitize.html')


@app.route('/submitPhoto', methods=['POST'])
def submitPhoto():
    b64 = request.form['img']

    file_id = str(uuid.uuid4())
    filename = f'{file_id}.png'
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    with open(path, 'wb') as f:
        f.write(base64.b64decode(b64[22:]))

    return redirect(url_for('digitize_page'))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        app.run()
    else:
        if sys.argv[1] == 'create_db':
            dbm.create_db()
