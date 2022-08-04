"""API of the website"""
import os
from flask import Blueprint
from flask_restx import Api
from app.definitions import routing

api = Api(
  version=os.environ['API_VERSION'],
  title='API of Personal Website 001',
  description='You found the api description.',
  validate=True,
)

bl_api = Blueprint('api', __name__, url_prefix=routing.get('api', 'prefix'))
