"""API of the website"""
import os
from flask import Blueprint
from flask_restx import Api
from app.definitions import routing

api = Api(
    version=os.environ['API_VERSION'],
    title='API of Personal Website',
    description='The api of the website.',
    validate=True,
)

bl_api = Blueprint('api', __name__, url_prefix=routing.get('api', 'prefix'))
