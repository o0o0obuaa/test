import flask
import flask.ext.login as flask_login
import os

from flask.ext.bootstrap import Bootstrap


app = flask.Flask(__name__)
app.secret_key = 'super secret string'


login_manager = flask_login.LoginManager()
login_manager.init_app(app)

bootstrap=Bootstrap(app)

from app import views, models






