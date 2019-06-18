"""User Controller"""
import os
import datetime
import flask_login
from flask import Blueprint, current_app
from flask_restful import Api, Resource, abort
from flask_sqlalchemy import sqlalchemy
from app.models.User import User as UserModel
from app.forms.login import LOGIN_PARSER
from app.forms.registration import REGISTRATION_PARSER

BLUE = Blueprint('user', __name__)
API = Api(BLUE)

class Login(Resource):
    """Log in"""
    def post(self):
        """Tries to login user with username and password"""
        args = LOGIN_PARSER.parse_args(strict=True)
        user = UserModel.query.filter_by(username=args.username).first()
        if user:
            current_date = datetime.datetime.utcnow()
            DB = current_app.config['user.db']
            if (current_date - user.last_try).total_seconds() > UserModel.LOGIN_COUNT_RESET:
                user.login_count = 0
            else:
                user.login_count = user.login_count + 1
            user.last_try = current_date
            DB.session.commit()
            if user.login_count < UserModel.LOGIN_COUNT_LIMIT:
                if user.is_password_correct(args.password):
                    user.login_count = 0
                    DB.session.commit()
                    flask_login.login_user(user) # flask_login logins the user
                    return 'You are now logged in!'
        abort(401)

class Logout(Resource):
    """Log out"""
    @flask_login.login_required
    def get(self):
        """Logs out user with the session"""
        flask_login.logout_user()
        return 'You are now logged out!'

class Register(Resource):
    """Register new user"""
    def post(self):
        args = REGISTRATION_PARSER.parse_args(strict=True)
        new_user = UserModel(
            username=args.username,
            email=args.email,
            password_hash=UserModel.get_hashed_password(args.password),
        )
        DB = current_app.config['user.db']
        try:
            DB.session.add(new_user)
            DB.session.commit()
        except sqlalchemy.exc.IntegrityError:
            # TODO: log, probably not unique
            abort(500)
        return 'Success!'


if os.getenv('FLASK_ENV') == 'development':
    API.add_resource(Register, '/register')
API.add_resource(Login, '/login')
API.add_resource(Logout, '/logout')
