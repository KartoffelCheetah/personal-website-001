#pylint: disable=R0201
"""User Controller"""
import os
import datetime
import flask_login
from flask import current_app
from flask_restplus import Resource, abort
from flask_sqlalchemy import sqlalchemy
from app.models.user_entity import UserEntity
from app.forms.login import LoginSchema, LOGIN_DOC
from app.forms.registration import RegistrationSchema, REGISTER_DOC
from app.definitions import ROUTING
from app.models.api import API

USER_NAMESPACE = API.namespace(
    ROUTING['USER']['namespace'],
    description='User management',
)

@USER_NAMESPACE.route(ROUTING['USER']['LOGIN'])
class Login(Resource):
    """Endpoint"""
    @API.doc(body=LOGIN_DOC)
    def post(self):
        """Tries to login user with username and password"""
        schema = LoginSchema()
        new_login = schema.load(API.payload)
        user = UserEntity.query.filter_by(username=new_login.data['username']).first()
        if user:
            current_date = datetime.datetime.utcnow()
            database = current_app.config['database']
            if (current_date - user.last_try).total_seconds() > UserEntity.LOGIN_COUNT_RESET:
                user.login_count = 0
            else:
                user.login_count = user.login_count + 1
            user.last_try = current_date
            database.session.commit()
            if user.login_count < UserEntity.LOGIN_COUNT_LIMIT:
                if user.is_password_correct(new_login.data['password']):
                    user.login_count = 0
                    database.session.commit()
                    flask_login.login_user(user) # flask_login logins the user
                    return 'You are now logged in!'
        return abort(401)

@USER_NAMESPACE.route(ROUTING['USER']['LOGOUT'])
class Logout(Resource):
    """Endpoint"""
    @flask_login.login_required
    @API.doc(security='cookie')
    def get(self):
        """Logs out user with the session"""
        flask_login.logout_user()
        return 'You are now logged out!'

@USER_NAMESPACE.route(ROUTING['USER']['REGISTER'])
class Register(Resource):
    """Endpoint"""
    @API.doc(body=REGISTER_DOC)
    def post(self):
        """Registers new user"""
        if os.getenv('FLASK_ENV') == 'development':
            schema = RegistrationSchema()
            new_registration = schema.load(API.payload)
            new_user = UserEntity(
                username=new_registration.data['username'],
                email=new_registration.data['email'],
                password_hash=UserEntity.get_hashed_password(new_registration.data['password']),
            )
            database = current_app.config['database']
            try:
                database.session.add(new_user)
                database.session.commit()
            except sqlalchemy.exc.IntegrityError:
                # TODO: log, probably not unique
                return abort(500)
            return 'Success!'
        return abort(404)
