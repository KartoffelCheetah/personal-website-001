"""
Setting up login manager
"""
import os
from typing import Final
import flask_login

LOGIN_MANAGER: Final[flask_login.LoginManager] = flask_login.LoginManager()
LOGIN_MANAGER.session_protection = os.getenv('LOGIN_MANAGER_SESSION_PROTECTION')
