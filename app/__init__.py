#!.venv/bin/python3
"""Flask Application Server"""
import os
import pathlib
from typing import Union, Final
from flask import Flask
from app.models.db import db
from app.managers.env_manager import load_env
load_env()
from app.managers.login_manager import login_manager
from app.definitions import PROJECT_PATH
from app.models.user_entity import UserEntity
from app.models.api import api, bl_api
from app.controllers.image_resource import ns_img_res
from app.controllers.user import ns_user

def create_app() -> Flask:
    """Creates Flask application"""

    app: Final[Flask] = Flask(__name__)
    # NOTE: FLASK_ENV configuration value is set from ENVIRONMENT variable
    app.config.update(
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

    app.config['database'] = db

    if not app.secret_key or len(app.secret_key) < 100:
        raise ValueError('You need to set a proper SECRET KEY.')

    db.init_app(app)

    db.create_all(app=app)

    login_manager.init_app(app)

    api.init_app(bl_api)

    app.register_blueprint(bl_api)

    api.add_namespace(ns_user)

    api.add_namespace(ns_img_res)

    @login_manager.user_loader
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

    return app
