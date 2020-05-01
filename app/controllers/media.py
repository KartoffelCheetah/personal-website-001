#pylint: disable=R0201
"""Media Controller"""
from flask import current_app
from flask_restx import Resource, abort, fields
import flask_login
from marshmallow.exceptions import ValidationError
from flask_sqlalchemy import sqlalchemy
from app.models.media_entity import MediaEntity
from app.definitions import ROUTING
from app.models.api import API

MEDIA_NAMESPACE = API.namespace(
    ROUTING['MEDIA']['namespace'],
    description='Media management',
)

MEDIA_DOC = API.model('Media', {
    'src': fields.String(
        required=True,
        description='Needs to be unique.',
        example='my-image',
        pattern=r'^[a-zA-Z\d\-\_]+$',
        **MediaEntity.SRC_LENGTH,
    ),
    'title': fields.String(
        required=True,
        **MediaEntity.TITLE_LENGTH,
    ),
    'license': fields.String(
        required=True,
        example='MIT',
        **MediaEntity.LICENSE_LENGTH,
    ),
    'description': fields.String(
        required=False,
        **MediaEntity.DESCRIPTION_LENGTH,
    ),
    'height': fields.Integer(
        readonly=True,
    ),
    'width': fields.Integer(
        readonly=True,
    ),
})

@MEDIA_NAMESPACE.route(ROUTING['MEDIA']['LIST'])
class MediaList(Resource):
    """Handles media in bulk"""

    @API.marshal_with(MEDIA_DOC, as_list=True)
    def get(self):
        """Returns all media."""
        return MediaEntity.query.all()

    @flask_login.login_required
    @API.doc(security='cookie', body=MEDIA_DOC)
    @API.marshal_with(MEDIA_DOC, as_list=True)
    def post(self):
        """Adds a new media element."""
        try:
            new_media = MediaEntity(**API.payload, width=0, height=0)
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
        return [new_media]
