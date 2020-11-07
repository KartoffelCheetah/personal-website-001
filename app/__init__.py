#!.venv/bin/python3
"""Flask Application Server"""
import os
import pathlib
from typing import Union, Final
from flask import Flask
from app.models.db import DB
from app.managers.env_manager import load_env
load_env()
from app.managers.login_manager import LOGIN_MANAGER
from app.definitions import PROJECT_PATH
from app.models.user_entity import UserEntity
from app.models.api import API, API_BLUEPRINT
from app.controllers.image_resource import IMAGE_RES_NAMESPACE
from app.controllers.user import USER_NAMESPACE

def create_app() -> Flask:
    """Creates Flask application"""

    APP: Final[Flask] = Flask(__name__)
    # NOTE: FLASK_ENV configuration value is set from ENVIRONMENT variable
    APP.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        SESSION_COOKIE_SECURE=bool(int(os.getenv('SESSION_COOKIE_SECURE'))),
        SESSION_COOKIE_HTTPONLY=bool(int(os.getenv('SESSION_COOKIE_HTTPONLY'))),
        REMEMBER_COOKIE_HTTPONLY=bool(int(os.getenv('REMEMBER_COOKIE_HTTPONLY'))),
        SQLALCHEMY_DATABASE_URI='sqlite:///'+str(PROJECT_PATH/os.getenv('DATABASE_NAME')),
        SQLALCHEMY_TRACK_MODIFICATIONS=bool(int(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))),
        PERMANENT_SESSION_LIFETIME=int(os.getenv('PERMANENT_SESSION_LIFETIME')),
        SESSION_COOKIE_NAME=os.getenv('SESSION_COOKIE_NAME'),
        SESSION_COOKIE_SAMESITE=os.getenv('SESSION_COOKIE_SAMESITE')
    )

    APP.config['database'] = DB

    if not APP.secret_key or len(APP.secret_key) < 100:
        raise ValueError('You need to set a proper SECRET KEY.')

    DB.init_app(APP)

    LOGIN_MANAGER.init_app(APP)

    API.init_app(API_BLUEPRINT)

    APP.register_blueprint(API_BLUEPRINT)

    API.add_namespace(USER_NAMESPACE)

    API.add_namespace(IMAGE_RES_NAMESPACE)

    DB.create_all(app=APP)

    @LOGIN_MANAGER.user_loader
    def load_user(user_identifier: str) -> Union[UserEntity, None]:
        """Gets user from session,
        if user_identifier is not valid returns None"""
        try:
            user_id, pwd_check = user_identifier.split('->')

            user = UserEntity.query.filter_by(id=int(user_id)).first()

            if user and user.session_auth(pwd_check):
                return user
        except ValueError:
            # ValueError: invalid input
            # just do not allow user to enter
            # TODO: logging
            pass
        return None

    return APP
