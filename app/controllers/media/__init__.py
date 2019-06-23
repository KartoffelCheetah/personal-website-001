"""Media Controller"""
from typing import Union
from flask import Blueprint, current_app
from flask_restful import Api, Resource, reqparse, abort
import flask_login
from flask_sqlalchemy import sqlalchemy
from app.models.Media import Media as MediaModel
from app.forms.add_media import ADD_MEDIA_PARSER

BLUE = Blueprint('media', __name__)
API = Api(BLUE)

class MediaList(Resource):
    """Handles media in bulk"""

    def get(self):
        """Returns all media."""
        medialist = MediaModel.query.all()
        return [media.title for media in medialist]

    @flask_login.login_required
    def post(self):
        """Adds new media element to media list."""
        args = ADD_MEDIA_PARSER.parse_args(strict=True)
        # TODO: calc width and height
        media = MediaModel(
            src=args.src,
            title=args.title,
            license=args.license,
            description=args.description,
            width=0,
            height=0)
        DB = current_app.config['media.db']
        try:
            DB.session.add(media)
            DB.session.commit()
        except sqlalchemy.exc.IntegrityError:
            # TODO log error
            abort(500)
        return 'Success!'

API.add_resource(MediaList, '/')
