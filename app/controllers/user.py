#pylint: disable=R0201
"""User Controller"""
import os
import datetime
import flask_login
from flask import current_app
from flask_restx import Resource, abort, fields
from flask_sqlalchemy import sqlalchemy
from app.models.user_entity import UserEntity
from app.definitions import ROUTING
from app.models.api import API

USER_NAMESPACE = API.namespace(
    ROUTING['USER']['namespace'],
    description='User management',
)

LOGIN_DOC = API.model('Login', {
    'username': fields.String(
        required=True,
        **UserEntity.USERNAME_LENGTH,
    ),
    'password': fields.String(
        required=True,
        **UserEntity.PASSWORD_LENGTH,
    ),
})

REGISTER_DOC = API.model('Register', {
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

@USER_NAMESPACE.route(ROUTING['USER']['LOGIN'])
class Login(Resource):
    """Endpoint"""

    @API.doc(body=LOGIN_DOC)
    def post(self):
        """Tries to login user with username and password"""
        current_app.logger.warning('Login attempt with username: %s', API.payload['username'])
        user = UserEntity.query.filter_by(username=API.payload['username']).first()
        if not user:
            current_app.logger.warning('No such user: %s', API.payload['username'])
            return abort(401)
        # user is found
        current_date = datetime.datetime.utcnow()
        database = current_app.config['database']
        if (current_date - user.last_try).total_seconds() > UserEntity.LOGIN_COUNT_RESET:
            user.login_count = 0
        else:
            user.login_count = user.login_count + 1
        user.last_try = current_date
        database.session.commit()
        if user.login_count < UserEntity.LOGIN_COUNT_LIMIT:
            if user.is_password_correct(API.payload['password']):
                user.login_count = 0
                database.session.commit()
                flask_login.login_user(user) # flask_login logins the user
                current_app.logger.warning('Successfull log in: %s', user)
                return {'message': 'You are now logged in!'}
            current_app.logger.warning('Invalid password during login: %s', user)
        return abort(401)

@USER_NAMESPACE.route(ROUTING['USER']['LOGOUT'])
class Logout(Resource):
    """Endpoint"""

    @flask_login.login_required
    @API.doc(security='cookie')
    def get(self):
        """Logs out user with the session"""
        flask_login.logout_user()
        return {'message': 'You are now logged out!'}

@USER_NAMESPACE.route(ROUTING['USER']['REGISTER'])
class Register(Resource):
    """Endpoint"""

    @API.doc(body=REGISTER_DOC)
    def post(self):
        """Registers new user"""
        if os.getenv('FLASK_ENV') == 'development':
            new_user = UserEntity(
                username=API.payload['username'],
                email=API.payload['email'],
                password_hash=UserEntity.get_hashed_password(API.payload['password']),
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
