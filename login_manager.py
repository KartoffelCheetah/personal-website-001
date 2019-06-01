"""
Setting up login manager
"""
import os
import flask_login
from dotenv import load_dotenv

from definitions import PROJECT_PATH

load_dotenv(dotenv_path=PROJECT_PATH/'.env.server', override=True)

LOGIN_MANAGER = flask_login.LoginManager()
LOGIN_MANAGER.session_protection = os.getenv('LOGIN_MANAGER_SESSION_PROTECTION')
