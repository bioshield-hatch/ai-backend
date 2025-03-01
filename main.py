from functools import wraps

from flask import Flask, request, render_template, flash, redirect, url_for, session
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, PasswordField, validators


app = Flask(__name__)


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized', 'danger')
            return redirect(url_for('login'))

    return wrap


def is_not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            flash('You are already logged in!', 'success')
            return redirect(url_for('login'))
        else:
            return f(*args, **kwargs)

    return wrap


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']




        if result > 0:
            # Get password

            # names = data['names_ids']

            if sha256_crypt.verify(password, hashed_password):
                # Set session variables
                session['logged_in'] = True
                session['username'] = username
                # session['names'] = names
                session['id'] = str(data['id'])
                print(session['username'])
                # print(session['names'])
                print(session['id'])
                print(session['logged_in'])

                print('PASS')
                return redirect(url_for('dashboard'))
            else:
                print('FAIL - INCORRECT PASSWORD')
                error = 'Invalid Login. Please check your username and/or password.'
                return render_template('login.html', error=error)

        else:
            print('FAIL - NO USER')
            error = 'Invalid Login. Please check your username and/or password.'
            return render_template('login.html', error=error)

    # If GET:
    return render_template('login.html')
