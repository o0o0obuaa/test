import flask
import flask.ext.login as flask_login
from flask_login import current_user,login_required,login_user
from flask import render_template, redirect, request, url_for, flash

from flask.ext.bootstrap import Bootstrap
from app import app,login_manager
from .models import User
from .forms import LoginForm, UploadForm, RunForm

from werkzeug.utils import secure_filename 
import os

users = {'qijun': {'pw': 'asdf'}}

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user



@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        passwd = form.password.data
        if username in users and users[username]['pw'] == passwd:
            user = User()
            user.id = username
            login_user(user)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')

    return render_template('login.html', form=form)

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form_1 = UploadForm()
    form_2 = RunForm()
    if  form_1.submit_upload.data and form_1.validate_on_submit():
        filename = secure_filename(form_1.script_file.data.filename)
        print filename
        print os.path.splitext(filename)[1]
        if os.path.splitext(filename)[1] == '.py':
            form_1.script_file.data.save('./app/upload/' + filename)
            flash('Upload Sucess!')
        else:
            filename = None
            flash('Invalid file or None')

    if form_2.submit_run.data:
        print 'fuck'
        flash('Running on the Spark!')

        
    return render_template('index.html', form_1=form_1, form_2 = form_2, name = current_user.id)

@app.route('/logout')
def logout():
    logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'




