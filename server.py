#!.venv/bin/python3
"""
Flask Application Server
"""
import os
import pathlib
from dotenv import load_dotenv
# flask
from flask import Flask
import flask_login
import jinja2
# models
from models.db import db
from models.User import User as UserModel
# blueprints
from app_media.routes import BLUE as mediaBlueprint
from app_user.routes import BLUE as userBlueprint
# ------------------------
# absolute path to project
PROJECT_PATH = pathlib.Path('.').absolute()
# Read the configuration
# and override ENVIRONMENT variables with dotenv
load_dotenv(dotenv_path=PROJECT_PATH/'.env', override=True)
load_dotenv(dotenv_path=PROJECT_PATH/'.env.blueprint', override=True)
# absolute path to database
DATABASE_PATH = PROJECT_PATH/os.getenv('DATABASE_NAME')
# ------------------------
APP = Flask(__name__)
# configure APP before doing anything noteworthy
# which could be influenced by the configuration
# NOTE: FLASK_ENV configuration value is set from ENVIRONMENT variable
APP.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    SESSION_COOKIE_SECURE=bool(int(os.getenv('SESSION_COOKIE_SECURE'))),
    SESSION_COOKIE_HTTPONLY=bool(int(os.getenv('SESSION_COOKIE_HTTPONLY'))),
    REMEMBER_COOKIE_HTTPONLY=bool(int(os.getenv('REMEMBER_COOKIE_HTTPONLY'))),
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE_PATH.__str__(),
    SQLALCHEMY_TRACK_MODIFICATIONS=bool(int(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))),
    PERMANENT_SESSION_LIFETIME=int(os.getenv('PERMANENT_SESSION_LIFETIME')),
    SESSION_COOKIE_NAME=os.getenv('SESSION_COOKIE_NAME'),
    SESSION_COOKIE_SAMESITE=os.getenv('SESSION_COOKIE_SAMESITE')
) # key has to be changed!
if len(APP.secret_key) < 100:
    raise ValueError('You need to set a proper SECRET KEY.')
# ##############################################
# DATABASE
db.init_app(APP)
# ###############################################
# LOGIN MANAGER
LOGIN_MANAGER = flask_login.LoginManager()
LOGIN_MANAGER.session_protection = os.getenv('LOGIN_MANAGER_SESSION_PROTECTION')
LOGIN_MANAGER.init_app(APP)
# ##############################################
# BLUEPRINTS
APP.register_blueprint(
    mediaBlueprint,
    url_prefix=os.getenv('MEDIA_BLUEPRINT_ENDPOINT'))
APP.register_blueprint(
    userBlueprint,
    url_prefix=os.getenv('USER_BLUEPRINT_ENDPOINT'))
# ##############################################
# DB-ACCESS
#   register db in config so media blueprint will
#   be able to access it from current_app.config
APP.config['media.db'] = db
# ##############################################
# JINJA2 CONFIGUTAION
@jinja2.contextfunction
def get_context(context):
    """Returns the context.
    Context is a 'Context object' of variables globally accessible to jinja2."""
    return context
# to render the context use '{{ _context() }}'
APP.add_template_global(name='_context', f=get_context)
# custom routes
APP.add_template_global(name='CUSTOM_ROUTES', f={
    'MEDIA_BLUEPRINT_ENDPOINT': os.getenv('MEDIA_BLUEPRINT_ENDPOINT'),
    'USER_BLUEPRINT_ENDPOINT': os.getenv('USER_BLUEPRINT_ENDPOINT')
})

# ##############################################
@APP.before_first_request
def create_tables():
    """Creates database and tables if they don't exist already."""
    db.create_all(app=APP)

@LOGIN_MANAGER.user_loader
def load_user(user_identifier):
    """Connects the flask_login User with the UserModel,
    if user_identifier is not valid returns None"""
    try:
        user_id, pwd_check = user_identifier.split('->')

        user = UserModel.query.filter_by(id=int(user_id)).first()

        if user and user.session_auth(pwd_check):
            return user
    except ValueError:
        # ValueError: invalid input
        # just do not allow user to enter
        # TODO: logging
        pass
    return None

#////////////////////////////////////
if __name__ == '__main__':
    # only run in main in development
    # production mode should import the APP
    APP.run(port=5000, host='0.0.0.0', threaded=True)
