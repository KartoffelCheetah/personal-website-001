"""API of the website"""
import os
from flask import Blueprint
from flask_restx import Api
from app.definitions import ROUTING

API = Api(
    version=os.getenv('API_VERSION'),
    title='API of Personal Website',
    description='The api of the website.',
    validate=True,
)

API_BLUEPRINT = Blueprint('api', __name__, url_prefix=ROUTING['API_PREFIX'])
