import os.path
from datetime import datetime, timedelta
import sqlalchemy.exc
from passlib.hash import sha256_crypt
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email
from os import urandom
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
app = Flask(__name__, static_url_path='', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, 'db.sqlite')
db = SQLAlchemy(app)
app.app_context().push()
SECRET_KEY = os.urandom(32)
# SECRET_KEY = "set value for testing"
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_COOKIE_SECURE'] = False  # Localhosting uses http not https
app.config['DEBUG'] = True
lm = LoginManager()
lm.init_app(app)
lm.login_view = "User/Add"
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(seconds=30)
