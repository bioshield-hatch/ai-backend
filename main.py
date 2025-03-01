import os
from functools import wraps
import requests
import json

from flask import Flask, request, render_template, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
from tf_utils import predict_image

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'pgp'}

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
            return redirect(url_for('secure_upload'))
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
        print(request.form)
        print(username, password)

        res = requests.post('http://127.0.0.1:8090/api/collections/users/auth-with-password',
                            data={'identity': username, 'password': password})
        login_data = json.loads(res.text)
        print(login_data)

        if 'record' in login_data:
            session['logged_in'] = True
            session['name'] = login_data['record']['name']
            session['id'] = login_data['record']['id']
            session['token'] = login_data['token']

            print('PASS')
            return redirect(url_for('secure_upload'))

        else:
            print('FAIL - INCORRECT PASSWORD')
            error = 'Invalid Login. Please check your username and/or password.'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
@is_not_logged_in
def signup():
    if request.method == 'POST':
        flash('Please contact an Administrator to create an account.', 'error')
    return render_template('signup.html')


@app.route('/logout', methods=['GET'])
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/secure_upload', methods=['GET', 'POST'])
@is_logged_in
def secure_upload():
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            res = requests.post('http://127.0.0.1:8090/api/collections/files/records',
                                headers={'Authorization': session['token']},
                                files={'file': file},
                                data={'name': file.filename, 'allowed_users': session['id']})
            print(res.text)

            if res.status_code == 200:
                flash('File uploaded!')
                return redirect(url_for('files'))

        flash('Invalid file name')
        return redirect(url_for('secure_upload'))

    res = requests.get('http://127.0.0.1:8090/api/collections/users/records',
                       headers={'Authorization': session['token']})
    users = json.loads(res.text)
    print(users)
    return render_template('secure_upload.html', users=users['items'])


@app.route('/files', methods=['GET'])
@is_logged_in
def files():
    res = requests.get('http://127.0.0.1:8090/api/collections/files/records',
                       headers={'Authorization': session['token']})
    file_list = json.loads(res.text)
    print(res.text)

    return render_template('files.html', files=file_list['items'])


@app.route('/download_file/<string:file_id>', methods=['GET'])
@is_logged_in
def download_file(file_id):
    res = requests.get('http://127.0.0.1:8090/api/collections/files/records/' + str(file_id),
                       headers={'Authorization': session['token']})
    file_info = json.loads(res.text)
    print(file_info)

    if 'file' in file_info:
        return redirect('http://127.0.0.1:8090/api/files/files/' + file_id + '/' + file_info['file'])
    else:
        flash('File not found')
        return redirect(url_for('files'))


@app.route('/diagnose_plant', methods=['GET', 'POST'])
@is_logged_in
def diagnose_plant():
    if request.method == "POST":
        file = request.files.get("file")
        filename = secure_filename(file.filename)
        filepath = os.path.join("static", app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        label, likelihood = predict_image(filepath)
        return render_template("diagnose_plant.html", filename=filename, label=label, confidence=likelihood * 100)
    return render_template("diagnose_plant.html", filename=None, label=None, confidence=None)


if __name__ == '__main__':
    # set_auth(mysql, clear=True)
    app.secret_key = "aoresntoufo8q934mplaum4b89(#W84lp0923puonwa"
    app.run(port=7546, host='127.0.0.1', debug=True)
