#pylint: disable=R0201
"""Image Resource Controller"""
import os
from werkzeug.datastructures import FileStorage
from flask import current_app
from flask_restx import Resource, abort, fields
import flask_login
from flask_sqlalchemy import sqlalchemy
from app.models.image_resource_entity import ImageResourceEntity
from app.definitions import ROUTING
from app.models.api import api
from app.managers.image_resource_manager import is_exists_in_db, is_exists_in_fs, get_securefname, get_securefpath, save_image_resource_to_fs

ns_img_res = api.namespace(
    ROUTING['RI']['IMAGE']['namespace'],
    description='Image resource management',
)

doc_image = api.model('ImageResource', {
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

doc_img_post = api.parser()
doc_img_post.add_argument(
        'resource',
        type=str,
        help='Unique resource identifier.',
        location='form',
        required=True
        )
doc_img_post.add_argument('imagedata', location='files', type=FileStorage, required=True)

@ns_img_res.route(ROUTING['RI']['IMAGE']['LIST'])
class ImageResourceList(Resource):
    """Handles image resources"""

    @api.marshal_with(doc_image, as_list=True)
    def get(self):
        """Returns all image resources."""
        return ImageResourceEntity.query.all()

    @flask_login.login_required
    @api.doc(security='cookie', body=doc_img_post)
    @api.expect(doc_img_post, as_list=True)
    @api.marshal_with(doc_image, as_list=True)
    def post(self):
        """Adds a new image resource."""
        args = doc_img_post.parse_args()

        securefname = get_securefname(args['resource'])

        if is_exists_in_db(securefname, current_app.logger) or is_exists_in_fs(securefname, current_app.logger):
            return abort(409)

        new_media = save_image_resource_to_fs(securefname, args['imagedata'])

        database = current_app.config['database']

        database.session.add(new_media)

        try:
            database.session.commit()

        except sqlalchemy.exc.IntegrityError:
            current_app.logger.exception('Post image resource - integrity error in db.')

            return abort(409)

        return [new_media]
