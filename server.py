#!.venv/bin/python3

import os
import pathlib
from os.path import splitext, dirname, abspath, join as pathJoin
from dotenv import load_dotenv
# flask
from flask import Flask, render_template, g, abort, redirect
from flask_restful import reqparse, abort, Resource, Api
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
if app.secret_key=='notsecure' or len(app.secret_key) < 100:
    raise ValueError('You need to set a proper SECRET KEY.')
# Plugins
api = Api(app)
db.init_app(app)
# Create db with tables
db.create_all(app=app)
#////////////////////////////////////
## ROUTES ##
# -----------------------------------------------
# TODO Userhandling with WTFORMS?
# TODO: add csrf tokens
# TODO: defend with auth
# TODO: sanitize input
# TODO: make decorator for only debug
class Users(Resource):
    """docstring for TODO"""
    def get(self):
        users = UserModel.query.all()
        return {'users': [{
            'username': user.username,
            'email': user.email,
        } for user in users if user]}
    def post(self): # TODO: this needs to be super secure
        parser = reqparse.RequestParser()
        parser.add_argument(
            'username',
            type=str,
            location='form',
            required=True,
        )
        parser.add_argument(
            'email',
            type=str,
            location='form',
            required=True,
        )
        parser.add_argument(
            'password',
            type=str,
            location='form',
            required=True,
        )
        args = parser.parse_args()
        print(args)
        # TODO do something
        return {}

class User(Resource):
    """docstring for TODO"""
    def get(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        return {'user':{
            'username': user.username,
            'email': user.email,
        } if user else user }


api.add_resource(Users, '/users')
api.add_resource(User, '/user/<int:user_id>')
#////////////////////////////////////
if __name__=='__main__':
    # only run in main in development
    # production mode should import the app
    app.run(threaded=True)
