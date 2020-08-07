#pylint: disable=R0201
"""Image Resource Controller"""
import os
from PIL import Image
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
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

IMAGE_POST_DOC = API.parser()
IMAGE_POST_DOC.add_argument(
        'resource',
        type=str,
        help='Unique resource identifier.',
        location='form',
        required=True
        )
IMAGE_POST_DOC.add_argument('imagedata', location='files', type=FileStorage, required=True)

@IMAGE_RES_NAMESPACE.route(ROUTING['RI']['IMAGE']['LIST'])
class ImageResourceList(Resource):
    """Handles image resources"""

    @API.marshal_with(IMAGE_DOC, as_list=True)
    def get(self):
        """Returns all image resources."""
        return ImageResourceEntity.query.all()

    @flask_login.login_required
    @API.doc(security='cookie', body=IMAGE_POST_DOC)
    @API.expect(IMAGE_POST_DOC, as_list=True)
    @API.marshal_with(IMAGE_DOC, as_list=True)
    def post(self):
        """Adds a new image resource."""
        is_conflict = False
        args = IMAGE_POST_DOC.parse_args()
        securefname = secure_filename(args['resource'])
        securefpath = os.path.join(os.getenv('FOLDER_UPLOAD'), securefname)
        if ImageResourceEntity.query.filter_by(resource=securefname).first():
            current_app.logger.exception('Post image resource image already exists in db.')
            is_conflict = True
        if os.path.exists(securefpath):
            current_app.logger.exception('Post image resource image already exists in fs.')
            is_conflict = True
        if is_conflict:
            return abort(409)
        args['imagedata'].save(securefpath)
        width, height = Image.open(securefpath).size
        new_media = ImageResourceEntity(resource=securefname, width=width, height=height)
        database = current_app.config['database']
        try:
            database.session.add(new_media)
            database.session.commit()
        except sqlalchemy.exc.IntegrityError:
            current_app.logger.exception('Post image resource integrity error in db.')
            return abort(409)
        return [new_media]
