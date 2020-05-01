"""API of the website"""
import os
from flask_restx import Api
import dotenv

dotenv.load_dotenv('../.env', override=True)

API = Api(
    version=os.getenv('API_VERSION'),
    title='API of Personal Website',
    description='The api of the website.',
)
