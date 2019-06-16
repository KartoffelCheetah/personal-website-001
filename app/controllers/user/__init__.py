"""User Controller"""
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, abort
import flask_login
from app.validators import max_length
from app.models.User import User as UserModel

BLUE = Blueprint('user', __name__)
API = Api(BLUE)

class Login(Resource):
    def post(self):
        """Expects username and pwd to login user"""
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument(
            'username',
            type=max_length(UserModel.USERNAME_LENGTH, str),
            required=True,
            location='form')
        parser.add_argument(
            'password',
            type=max_length(256, str),
            required=True,
            location='form')
        args = parser.parse_args(strict=True)
        user = UserModel.query.filter_by(username=args.username).first()
        if user and user.is_under_login_count_limit() and user.is_password_correct(args.password):
            user.login_count = 0
            flask_login.login_user(user) # flask_login logins the user
            return 'You are now logged in!'
        abort(401)

class Logout(Resource):
    """Logs out user"""
    @flask_login.login_required
    def get(self):
        """Logout user"""
        flask_login.logout_user()
        return 'You are now logged out!'

API.add_resource(Login, '/login')
API.add_resource(Logout, '/logout')
