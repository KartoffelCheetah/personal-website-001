#pylint: disable=R0201
"""Image Resource Controller"""
from flask import url_for
from flask_restx import Resource, fields
from app.models.image_resource_entity import ImageResourceEntity
from app.definitions import routing
from app.models.api import api
from app.managers.image_resource_manager import ImageProcess

ns_img_res = api.namespace(
  routing.get('namespace_image', 'namespace'),
  description='Image resource management',
)

_image_resource_model = api.model('ImageResource', {
  '@context': fields.String('https://schema.org', example='https://schema.org'),
  '@type': fields.String('ImageObject', example='ImageObject'),
  '@id': fields.String(
    attribute=lambda ire: url_for(
      'api.image_image_resource_resource_by_resource',
      name=ire.resource,
    ),
    example='/api/image/hello-example.png',
  ),
  'name': fields.String(attribute='resource'),
  'contentUrl': fields.String(
    attribute=lambda ire: ImageProcess(ire.resource).url,
    example='hello-example.png',
    **ImageResourceEntity.RI_LENGTH,
  ),
  'thumbnailUrl': fields.List(
    fields.String,
    attribute=lambda ire: [t.url for t in ImageProcess(ire.resource).thumbnails],
  ),
  'height': fields.Integer(),
  'width': fields.Integer()
})

_parser_get_images = api.parser()
_parser_get_images.add_argument('names', type=str, action='append', required=True)

@ns_img_res.route(routing.get('namespace_image', 'image')+'<name>')
class ImageResourceResourceByResource(Resource):
  """Handles a single image resource"""
  @api.marshal_with(_image_resource_model, as_list=False)
  def get(self, name):
    """Returns an image resource."""
    return ImageResourceEntity.query.filter_by(resource=name).first()

@ns_img_res.route(routing.get('namespace_image', 'image'))
class ImageResourceResource(Resource):
  """Handles multiple image resources"""
  @api.expect(_parser_get_images)
  @api.marshal_with(_image_resource_model, as_list=True)
  def get(self):
    """Returns all filtered image resources."""
    names = list(_parser_get_images.parse_args()['names'])
    return ImageResourceEntity.query.filter(ImageResourceEntity.resource.in_(names)).all()
