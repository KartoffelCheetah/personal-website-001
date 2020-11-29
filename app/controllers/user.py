#pylint: disable=R0201
"""User Controller"""
import os
from datetime import datetime
from typing import Final
import flask_login
from flask import current_app
from flask_restx import Resource, abort, fields
from flask_sqlalchemy import sqlalchemy
from app.models.user_entity import UserEntity
from app.definitions import ROUTING
from app.models.api import api
from app.managers.user_manager import tick_user_login_count, is_user_below_max_login_count

ns_user: Final[api.namespace] = api.namespace(
    ROUTING['USER']['namespace'],
    description='User management',
)

doc_login: Final[api.model] = api.model('Login', {
    'username': fields.String(
        required=True,
        **UserEntity.USERNAME_LENGTH,
    ),
    'password': fields.String(
        required=True,
        **UserEntity.PASSWORD_LENGTH,
    ),
})

doc_register: Final[api.model] = api.model('Register', {
    'username': fields.String(
        required=True,
        **UserEntity.USERNAME_LENGTH,
    ),
    'password': fields.String(
        required=True,
        **UserEntity.PASSWORD_LENGTH,
    ),
    'email': fields.String(
        required=True,
        **UserEntity.EMAIL_LENGTH,
    ),
})

@ns_user.route(ROUTING['USER']['LOGIN'])
class Login(Resource):
    """Endpoint"""

    @api.doc(body=doc_login)
    def post(self):
        """Tries to login user with username and password"""
        current_app.logger.warning('Login attempt with username: %s', api.payload['username'])
        user = UserEntity.query.filter_by(username=api.payload['username']).first()
        if not user:
            current_app.logger.warning('No such user: %s', api.payload['username'])
            return abort(401)
        # user is found
        current_date = datetime.utcnow()
        database = current_app.config['database']
        tick_user_login_count(user)
        user.last_try = current_date
        database.session.commit()
        if is_user_below_max_login_count(user):
            if user.is_password_correct(api.payload['password']):
                user.login_count = 0
                database.session.commit()
                flask_login.login_user(user) # flask_login logins the user
                current_app.logger.warning('Successfull log in: %s', user)
                return {'message': 'You are now logged in!'}
            current_app.logger.warning('Invalid password during login: %s', user)
        return abort(401)

@ns_user.route(ROUTING['USER']['LOGOUT'])
class Logout(Resource):
    """Endpoint"""

    @flask_login.login_required
    @api.doc(security='cookie')
    def get(self):
        """Logs out user with the session"""
        flask_login.logout_user()
        return {'message': 'You are now logged out!'}

@ns_user.route(ROUTING['USER']['REGISTER'])
class Register(Resource):
    """Endpoint"""

    @api.doc(body=doc_register)
    def post(self):
        """Registers new user"""
        if os.getenv('FLASK_ENV') == 'development':
            new_user = UserEntity(
                username=api.payload['username'],
                email=api.payload['email'],
                password_hash=UserEntity.get_hashed_password(api.payload['password']),
            )
            database = current_app.config['database']
            try:
                database.session.add(new_user)
                database.session.commit()
            except sqlalchemy.exc.IntegrityError:
                current_app.logger.exception('Registration integrity error in db.')
                return abort(500)
            current_app.logger.warning('New user is successfully registered: %s', new_user)
            return {'message': 'Registered!'}
        return abort(404)
