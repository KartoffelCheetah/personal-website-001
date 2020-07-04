#pylint: disable=R0201
"""Image Resource Controller"""
from flask import current_app
from flask_restx import Resource, abort, fields
import flask_login
from flask_sqlalchemy import sqlalchemy
from app.models.image_resource_entity import ImageResourceEntity
from app.definitions import ROUTING
from app.models.api import API

IMAGE_RES_NAMESPACE = API.namespace(
    ROUTING['RI']['IMAGE']['namespace'],
    description='Image resource management',
)

IMAGE_DOC = API.model('ImageResource', {
    'resource': fields.String(
        required=True,
        description='Unique resource identifier.',
        example='my-image',
        pattern=ImageResourceEntity.RI_PATTERN,
        **ImageResourceEntity.RI_LENGTH,
    ),
    'height': fields.Integer(
        readonly=True,
    ),
    'width': fields.Integer(
        readonly=True,
    ),
})

@IMAGE_RES_NAMESPACE.route(ROUTING['RI']['IMAGE']['LIST'])
class ImageResourceList(Resource):
    """Handles image resources"""

    @API.marshal_with(IMAGE_DOC, as_list=True)
    def get(self):
        """Returns all image resources."""
        return ImageResourceEntity.query.all()

    @flask_login.login_required
    @API.doc(security='cookie', body=IMAGE_DOC)
    @API.marshal_with(IMAGE_DOC, as_list=True)
    def post(self):
        """Adds a new image resource."""
        new_media = ImageResourceEntity(**API.payload, width=0, height=0)
        database = current_app.config['database']
        try:
            database.session.add(new_media)
            database.session.commit()
        except sqlalchemy.exc.IntegrityError:
            current_app.logger.exception('Post image resource integrity error in db.')
            return abort(409)
        return [new_media]
