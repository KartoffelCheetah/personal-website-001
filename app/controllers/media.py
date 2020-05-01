#pylint: disable=R0201
"""Media Controller"""
from flask import current_app
from flask_restx import Resource, abort
import flask_login
from marshmallow.exceptions import ValidationError
from flask_sqlalchemy import sqlalchemy
from app.models.media_entity import MediaEntity
from app.forms.add_media import MediaSchema, MEDIA_DOC
from app.definitions import ROUTING
from app.models.api import API

MEDIA_NAMESPACE = API.namespace(
    ROUTING['MEDIA']['namespace'],
    description='Media management',
)

@MEDIA_NAMESPACE.route(ROUTING['MEDIA']['LIST'])
class MediaList(Resource):
    """Handles media in bulk"""

    def get(self):
        """Returns all media."""
        medialist = MediaEntity.query.all()
        return [
            {
                'src': media.src,
                'title': media.title,
                'license': media.license,
                'description': media.description,
                'width': media.width,
                'height': media.height
            }
            for media in medialist
        ]

    @flask_login.login_required
    @API.doc(security='cookie', body=MEDIA_DOC)
    def post(self):
        """Adds a new media element."""
        schema = MediaSchema()
        try:
            new_media = schema.load(API.payload)
        except ValidationError as error:
            current_app.logger.warning('Invalid media form.')
            return abort(400, message=error)
        database = current_app.config['database']
        try:
            database.session.add(new_media)
            database.session.commit()
        except sqlalchemy.exc.IntegrityError as error:
            current_app.logger.exception('Post media integrity error in db.')
            return abort(409)
        return 'Success!'
