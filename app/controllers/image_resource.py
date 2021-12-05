#pylint: disable=R0201
"""Image Resource Controller"""
import os
import re
from werkzeug.datastructures import FileStorage
from flask import current_app, url_for
from flask_restx import Resource, abort, fields
import flask_login
from flask_sqlalchemy import sqlalchemy
from app.models.image_resource_entity import ImageResourceEntity
from app.definitions import routing
from app.models.api import api
from app.managers.image_resource_manager import is_conflicting, get_securefname, ImageProcess, save_image_resource_to_fs, get_image_resource_entity_from_fs
from app.controllers._flask_utils import only_development

ns_img_res = api.namespace(
  routing.get('namespace_image', 'namespace'),
  description='Image resource management',
)

image_resource_model = api.model('ImageResource', {
  '@context': fields.String('https://schema.org', example='https://schema.org'),
  '@type': fields.String('ImageObject', example='ImageObject'),
  '@id': fields.String(
    attribute=lambda ire: url_for('api.image_image_resource_resource_by_resource', name=ire.resource),
    example='/api/image/my-image.png',
  ),
  'name': fields.String(attribute='resource'),
  'contentUrl': fields.String(
    attribute=lambda ire: ImageProcess(ire.resource).url,
    example='my-image.png',
    pattern=ImageResourceEntity.RI_PATTERN,
    **ImageResourceEntity.RI_LENGTH,
  ),
  'thumbnailUrl': fields.List(
    fields.String,
    attribute=lambda ire: [t.url for t in ImageProcess(ire.resource).thumbnails],
  ),
  'height': fields.Integer(),
  'width': fields.Integer()
})

post_image_parser = api.parser()
post_image_parser.add_argument('name', location='form', type=str, required=False)
post_image_parser.add_argument('imagedata', location='files', type=FileStorage, required=True)

@ns_img_res.route(routing.get('namespace_image', 'image')+'<name>')
class ImageResourceResourceByResource(Resource):
  """Handles image resources"""
  @api.marshal_with(image_resource_model, as_list=True)
  def get(self, name):
    """Returns image resource."""
    return ImageResourceEntity.query.filter_by(resource=name).all()

@ns_img_res.route(routing.get('namespace_image', 'image'))
class ImageResourceResource(Resource):
  """Handles image resources"""

  @api.marshal_with(image_resource_model, as_list=True)
  def get(self):
    """Returns all image resources."""
    return ImageResourceEntity.query.all()

  @flask_login.login_required
  @api.doc(security='cookie', body=post_image_parser)
  @api.expect(post_image_parser, as_list=True)
  @api.marshal_with(image_resource_model, as_list=True)
  @only_development
  def post(self):
    """Adds a new image resource."""
    args = post_image_parser.parse_args()

    filename = args['name'] or args['imagedata'].filename

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
