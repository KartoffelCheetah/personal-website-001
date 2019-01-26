#!.venv/bin/python3

import os
import pathlib
from os.path import splitext, dirname, abspath, join as pathJoin
from dotenv import load_dotenv
# flask
from flask import (
                    Flask,
                    g,
                    session,
                    render_template,
                    make_response,
                    redirect,
                    abort,
                    jsonify)
from flask_restful import reqparse, abort, Resource, Api
import flask_login
import jinja2
# models
from models.db import db
from models.User import User as UserModel
from models.Media import Media as MediaModel
# blueprints
from app_media.routes import blue as mediaBlueprint
from app_user.routes import blue as userBlueprint
# ------------------------
# absolute path to project
PROJECT_PATH = pathlib.Path('.').absolute()
# Read the configuration
# and override ENVIRONMENT variables with dotenv
load_dotenv(dotenv_path=PROJECT_PATH/'.env', override=True)
# absolute path to database
DATABASE_PATH = PROJECT_PATH/os.getenv('DATABASE_NAME')
# ------------------------
app = Flask(__name__)
# configure app before doing anything noteworthy
# which could be influenced by the configuration
# NOTE: FLASK_ENV configuration value is set from ENVIRONMENT variable
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    SESSION_COOKIE_SECURE=bool(int(os.getenv('SESSION_COOKIE_SECURE'))),
    SESSION_COOKIE_HTTPONLY=bool(int(os.getenv('SESSION_COOKIE_HTTPONLY'))),
    REMEMBER_COOKIE_HTTPONLY = bool(int(os.getenv('REMEMBER_COOKIE_HTTPONLY'))),
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE_PATH.__str__(),
    SQLALCHEMY_TRACK_MODIFICATIONS=bool(int(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))),
    PERMANENT_SESSION_LIFETIME=int(os.getenv('PERMANENT_SESSION_LIFETIME')),
    SESSION_COOKIE_NAME=os.getenv('SESSION_COOKIE_NAME'),
    SESSION_COOKIE_SAMESITE=os.getenv('SESSION_COOKIE_SAMESITE')
) # key has to be changed!
if len(app.secret_key) < 100:
    raise ValueError('You need to set a proper SECRET KEY.')
# RESTAPI
api = Api(app, prefix=os.getenv('API_PREFIX'))
# ##############################################
# DATABASE
db.init_app(app)
# ###############################################
# LOGIN MANAGER
login_manager = flask_login.LoginManager()
login_manager.session_protection = os.getenv('LOGIN_MANAGER_SESSION_PROTECTION')
login_manager.init_app(app)
# ##############################################
# BLUEPRINTS
app.register_blueprint(
    mediaBlueprint,
    url_prefix=os.getenv('MEDIA_BLUEPRINT_ENDPOINT'))
app.register_blueprint(
    userBlueprint,
    url_prefix=os.getenv('USER_BLUEPRINT_ENDPOINT'))
# ##############################################
# DB-ACCESS
#   register db in config so media blueprint will
#   be able to access it from current_app.config
app.config['media.db'] = db
# ##############################################
# JINJA2 CONFIGUTAION
@jinja2.contextfunction
def get_context(c):
    """Returns the context.
    Context is a 'Context object' of variables globally accessible to jinja2.
    To get the context in templates use {{ context() }}"""
    return c

app.jinja_env.globals['context'] = get_context

(app.jinja_env.globals
    ['MEDIA_BLUEPRINT_ENDPOINT']) = os.getenv('MEDIA_BLUEPRINT_ENDPOINT')

(app.jinja_env.globals
    ['USER_BLUEPRINT_ENDPOINT']) = os.getenv('USER_BLUEPRINT_ENDPOINT')
# ##############################################

@app.before_first_request
def create_tables():
    """Creates database and tables if they don't exist already."""
    db.create_all(app=app)

@login_manager.user_loader
def load_user(user_identifier):
    """Connects the flask_login User with the UserModel,
    if user_identifier is not valid returns None"""
    try:
        user_id, pwdCheck = user_identifier.split('->')

        user = UserModel.query.filter_by(id=int(user_id)).first()

        if user and user.session_auth(pwdCheck):
            return user
    except ValueError:
        # ValueError: invalid input
        # just do not allow user to enter
        # TODO: logging
        pass
    return None

#////////////////////////////////////
## ROUTES ##
# -----------------------------------------------

@app.route('/login_page')
def login_page():
    return render_template('login_page.html.j2')

# register API endponints

#////////////////////////////////////
if __name__=='__main__':
    # only run in main in development
    # production mode should import the app
    app.run(port=5000, host='0.0.0.0', threaded=True)
