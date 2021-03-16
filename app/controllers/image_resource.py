#pylint: disable=R0201
"""Image Resource Controller"""
import os
import re
from werkzeug.datastructures import FileStorage
from flask import current_app
from flask_restx import Resource, abort, fields
import flask_login
from flask_sqlalchemy import sqlalchemy
from app.models.image_resource_entity import ImageResourceEntity
from app.definitions import routing
from app.models.api import api
from app.managers.image_resource_manager import is_conflicting, get_securefname, save_image_resource_to_fs, get_image_resource_entity_from_fs

ns_img_res = api.namespace(
    routing.get('namespace_image', 'namespace'),
    description='Image resource management',
)

doc_img = api.model('ImageResource', {
    '@context': fields.String(
        'https://schema.org',
        example='https://schema.org',
        readonly=True,
    ),
    '@type': fields.String(
        'ImageObject',
        example='ImageObject',
        readonly=True,
    ),
    'contentUrl': fields.String(
        attribute='resource',
        required=False,
        description='Unique resource identifier.',
        example='my-image.png',
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
    location='form',
    required=False,
    help='Unique resource identifier.',
)
doc_img_post.add_argument('imagedata', location='files', type=FileStorage, required=True)

@ns_img_res.route(routing.get('namespace_image', 'image')+'<contentUrl>')
class ImageResourceResourceByResource(Resource):
    """Handles image resources"""
    @api.marshal_with(doc_img, as_list=True)
    def get(self, contentUrl):
        """Returns image resource."""
        return ImageResourceEntity.query.filter_by(resource=contentUrl).all()

@ns_img_res.route(routing.get('namespace_image', 'image'))
class ImageResourceResource(Resource):
    """Handles image resources"""

    @api.marshal_with(doc_img, as_list=True)
    def get(self):
        """Returns all image resources."""
        return ImageResourceEntity.query.all()

    @flask_login.login_required
    @api.doc(security='cookie', body=doc_img_post)
    @api.expect(doc_img_post, as_list=True)
    @api.marshal_with(doc_img, as_list=True)
    def post(self):
        """Adds a new image resource."""
        args = doc_img_post.parse_args()

        filename = args['resource'] or args['imagedata'].filename

        if not re.match(ImageResourceEntity.RI_PATTERN, filename):
            return abort(400, f'Filename does not conform to {ImageResourceEntity.RI_PATTERN}')
        if not ImageResourceEntity.RI_LENGTH['min_length'] < len(filename) < ImageResourceEntity.RI_LENGTH['max_length']:
            return abort(400, 'Filename length does not conform to length')
        if not os.path.splitext(filename)[1]:
            return abort(400, 'Filename extension missing')

        securefname = get_securefname(filename)

        if is_conflicting(securefname, current_app.logger):
            return abort(409)

        save_image_resource_to_fs(securefname, args['imagedata'])

        new_media = get_image_resource_entity_from_fs(securefname)

        database = current_app.config['database']

        database.session.add(new_media)

        try:
            database.session.commit()

        except sqlalchemy.exc.IntegrityError:
            current_app.logger.exception('Post image resource - integrity error in db.')

            return abort(409)

        return [new_media]
