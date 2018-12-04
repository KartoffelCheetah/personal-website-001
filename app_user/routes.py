from flask import Blueprint
from flask_restful import Api, Resource, reqparse, abort
import flask_login

from validator import max_length
# models
from models.User import User as UserModel

blue = Blueprint('user', __name__)
api = Api(blue)

class Login(Resource):
    def post(self):
        """Expects username and pwd to login user"""
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument('username',
            type=max_length(64, str),
            required=True,
            location='form')
        parser.add_argument('password',
            type=max_length(1024, str),
            required=True,
            location='form')
        args = parser.parse_args(strict=True)
        user = UserModel.query.filter_by(username=args.username).first()
        if user and user.verify_password_hash(args.password):
            flask_login.login_user(user) # flask_login logins the user
            return 'You are now logged in!'
        abort(401)

class Logout(Resource):
    @flask_login.login_required
    def get(self):
        """Logout user"""
        flask_login.logout_user()
        return 'You are now logged out!'

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
