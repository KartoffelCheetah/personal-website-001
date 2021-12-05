#!.venv/bin/python3
"""Flask Application Server"""
import os
import pathlib
from typing import Union, Final
from flask import Flask, Response, request
from app.models.db import db
import app.managers.env_manager # loads envs as a side-effect before other imports
from app.definitions import PROJECT_PATH
from app.models.api import api, bl_api
from app.controllers.image_resource import ns_img_res
from app.commands.image_resource_command import image_cli_group

def create_app() -> Flask:
  """Returns the Flask application"""

  app: Final[Flask] = Flask(__name__)
  # NOTE: FLASK_ENV configuration value is set from ENVIRONMENT variable
  app.config.update(
    SECRET_KEY=os.environ['SECRET_KEY'],
    SESSION_COOKIE_SECURE=bool(int(os.environ['SESSION_COOKIE_SECURE'])),
    SESSION_COOKIE_HTTPONLY=bool(int(os.environ['SESSION_COOKIE_HTTPONLY'])),
    REMEMBER_COOKIE_HTTPONLY=bool(int(os.environ['REMEMBER_COOKIE_HTTPONLY'])),
    SQLALCHEMY_DATABASE_URI='sqlite:///'+str(PROJECT_PATH/os.environ['DATABASE_NAME']),
    SQLALCHEMY_TRACK_MODIFICATIONS=bool(int(os.environ['SQLALCHEMY_TRACK_MODIFICATIONS'])),
    PERMANENT_SESSION_LIFETIME=int(os.environ['PERMANENT_SESSION_LIFETIME']),
    SESSION_COOKIE_NAME=os.environ['SESSION_COOKIE_NAME'],
    SESSION_COOKIE_SAMESITE=os.environ['SESSION_COOKIE_SAMESITE']
  )

  app.config['database'] = db

  if not app.secret_key or len(app.secret_key) < 100:
    raise ValueError('You need to set a proper SECRET KEY.')

  db.init_app(app)

  db.create_all(app=app)

  api.init_app(bl_api)

  app.register_blueprint(bl_api)

  api.add_namespace(ns_img_res)

  app.cli.add_command(image_cli_group)

  @app.after_request
  def add_cors_headers(response: Response) -> Response:# pylint: disable=unused-variable
    if request.headers.get('origin') in os.environ['CORS_ACAO'].split('|'):
      response.headers.add('Access-Control-Allow-Origin', request.headers['origin'])
    return response

  return app
