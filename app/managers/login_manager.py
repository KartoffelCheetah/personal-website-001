"""
Setting up login manager
"""
import os
from typing import Final
import flask_login

login_manager: Final[flask_login.LoginManager] = flask_login.LoginManager()
login_manager.session_protection = os.environ['LOGIN_MANAGER_SESSION_PROTECTION']
