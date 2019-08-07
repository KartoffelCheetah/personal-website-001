"""Media Controller"""
from typing import Union
from flask import current_app
from flask_restplus import Resource, abort
import flask_login
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
        return [media.title for media in medialist]

    @flask_login.login_required
    @API.doc(security='cookie', body=MEDIA_DOC)
    def post(self):
        """Adds new media element to media list."""
        schema = MediaSchema()
        new_media = schema.load(API.payload)
        DB = current_app.config['media.db']
        try:
            DB.session.add(new_media.data)
            DB.session.commit()
        except sqlalchemy.exc.IntegrityError:
            # TODO log error
            abort(500)
        return 'Success!'
