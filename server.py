#!.venv/bin/python3
"""
Flask Application Server
"""
import os
from dotenv import load_dotenv
# flask
from flask import Flask
import jinja2
# models
from app.models.db import DB
from app.models.User import User as UserModel
# blueprints
from app.controllers.media import BLUE as MEDIA_BLUEPRINT
from app.controllers.user import BLUE as USER_BLUEPRINT
# login manager
from login_manager import LOGIN_MANAGER
# absolute path to project
from app.definitions import PROJECT_PATH, ROUTING
# ------------------------
# Read the configuration
# and override ENVIRONMENT variables with dotenv
load_dotenv(dotenv_path=PROJECT_PATH/'.env.server', override=True)
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
DB.init_app(APP)
# ###############################################
# LOGIN MANAGER
LOGIN_MANAGER.init_app(APP)
# ##############################################
# BLUEPRINTS
APP.register_blueprint(
    MEDIA_BLUEPRINT,
    url_prefix=ROUTING['MEDIA']['base'])
APP.register_blueprint(
    USER_BLUEPRINT,
    url_prefix=ROUTING['USER']['base'])
# ##############################################
# DB-ACCESS
#   register db in config so blueprint will
#   be able to access it from current_app.config
APP.config['media.db'] = DB
APP.config['user.db'] = DB
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
    'routing': ROUTING,
})

# ##############################################
@APP.before_first_request
def create_tables():
    """Creates database and tables if they don't exist already."""
    DB.create_all(app=APP)

@LOGIN_MANAGER.user_loader
def load_user(user_identifier):
    """Gets user from session,
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
