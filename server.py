#!.venv/bin/python3

import os
import pathlib
from os.path import splitext, dirname, abspath, join as pathJoin
from dotenv import load_dotenv
# token
from itsdangerous import (
                        BadSignature,
                        SignatureExpired,
                        TimedJSONWebSignatureSerializer as TJWSSerializer)
# flask
from flask import Flask, render_template, g, abort, redirect, jsonify
from flask_restful import reqparse, abort, Resource, Api
from flask_httpauth import HTTPTokenAuth
# models
from models.db import db
from models.User import User as UserModel
# ------------------------
# absolute path to project
PROJECT_PATH = pathlib.Path('.').absolute()
# Read the configuration
# and override ENVIRONMENT variables with dotenv
load_dotenv(dotenv_path=PROJECT_PATH/'.env', override=True)
# absolute path to database
DATABASE_PATH = PROJECT_PATH/os.getenv('DATABASE_NAME')
# ------------------------
app = Flask(__name__)
# configure app before doing anything noteworthy
# which could be influenced by the configuration
# NOTE: FLASK_ENV configuration value is set from ENVIRONMENT variable
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    SESSION_COOKIE_SECURE=os.getenv('SESSION_COOKIE_SECURE'),
    SQLALCHEMY_DATABASE_URI='sqlite:///'+DATABASE_PATH.__str__(),
    SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'),
) # key has to be changed!
if len(app.secret_key) < 100:
    raise ValueError('You need to set a proper SECRET KEY.')
# Plugins
api = Api(app, prefix='/api/v1')
db.init_app(app)
auth = HTTPTokenAuth(scheme='Token')

@app.before_first_request
def create_tables():
    """Creates database and tables if they don't exist already."""
    db.create_all(app=app)

@auth.verify_token
def verify(token):
    """Checks request's Authorization header for token."""
    return True if UserModel.verify_auth_token(app.secret_key, token) else False

#////////////////////////////////////
## ROUTES ##
# -----------------------------------------------
class Private_Test(Resource):
    @auth.login_required
    def get(self):
    #     db.session.add(
    #         UserModel(
    #             username='test',
    #             email='test@mail.com',
    #             password_hash=UserModel.hash_password('test'),
    #         )
    #     )
    #     db.session.commit()
        print('working')
        return
class Auth_Token(Resource):
    def post(self):
        """Expects username and pwd and returns token"""
        parser = reqparse.RequestParser()
        parser.add_argument('username',
            type=str,
            required=True,
            location='form')
        parser.add_argument('password',
            type=str,
            required=True,
            location='form')
        args = parser.parse_args()
        user = UserModel.query.filter_by(username=args.username).first()
        if user and user.verify_password_hash(args.password):
            token = user.generate_auth_token(app.secret_key)
            return jsonify({ 'token': token.decode('ascii') })
        abort(401)
# register API endponints
api.add_resource(Auth_Token, '/auth_token')
api.add_resource(Private_Test, '/pr')
#////////////////////////////////////
if __name__=='__main__':
    # only run in main in development
    # production mode should import the app
    app.run(threaded=True)
