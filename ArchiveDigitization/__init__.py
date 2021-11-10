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
import json

from util import db, helpers, digitize
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
        return redirect(url_for('login_page'))


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
        return redirect(url_for('register_page'))
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


@app.route('/digitized')
def digitized_page():
    imgs = dbm.get_files(True, True)
    return render_template('digitized.html', imgs=imgs)


@app.route('/submitPhoto', methods=['POST'])
def submitPhoto():
    img = request.files['actualImage']
    category = request.form['category']

    file_id = str(uuid.uuid4())
    filename = f'{file_id}.png'
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    img.save(path)

    dbm.add_file(file_id, category)

    return 'sigh'


@app.route('/doDigitization')
def doDigitization():
    cwd = os.getcwd()
    dbm = db.DBManager(app.config['DATABASE_URI'],
                       f'{cwd}/static/table_definitions.sql')
    digitize.main(dbm, os.path.split(app.config['STATIC_FOLDER'])[0])

    return 'All done!'


@app.route('/addTag', methods=['POST'])
def addTag():
    print(request.form)
    # Splitting on commas if any values selected, otherwise empty list
    selected = request.form['selected']
    selected = ','.split(selected) if selected != '' else []

    # Name for new tag
    tag_name = request.form['newTag']

    success, tag_id = dbm.create_tag(tag_name)

    if not success:
        pass

    # Get and process tags
    tags = dbm.get_all_tags()

    tags = [tag + [True] if tag[1] in selected of tag[1] == tag_name
            else tag + [False]
            for tag in tags]

    tags = sorted(tags, key=lambda x: x[2], reverse=True)

    return tags, [tag for tag in tags if tag[2]]

    # need to return the options tags already selected, and the new tag


if __name__ == '__main__':
    if len(sys.argv) == 1:
        app.run()
    else:
        if sys.argv[1] == 'create_db':
            dbm.create_db()
        elif sys.argv[1] == 'sql_command':
            if len(sys.argv) > 3:
                print('Too many args. Encase command in quotes!')
            else:
                dbm.raw_command(sys.argv[2])
