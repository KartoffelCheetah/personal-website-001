#pylint: disable=R0201
"""Image Resource Controller"""
from flask import url_for, abort
from flask_restx import Resource, fields
from app.models.image_resource_entity import ImageResourceEntity
from app.definitions import routing
from app.models.api import api_website
from app.managers.image_resource_manager import ImageProcess

ns_img_res = api_website.namespace(
  routing.get('namespace_image', 'namespace'),
  description='Image resource management',
)

_image_resource_model = api_website.model('ImageResource', {
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

_parser_get_images = api_website.parser()
_parser_get_images.add_argument('names', type=str, action='append', required=True)

@ns_img_res.route(routing.get('namespace_image', 'image')+'<name>')
class ImageResourceResourceByResource(Resource):
  """Handles a single image resource"""
  @api_website.marshal_with(_image_resource_model, as_list=False)
  def get(self, name):
    """Returns an image resource."""
    image_resource = ImageResourceEntity.query.filter_by(resource=name).first()
    if image_resource:
      return image_resource
    else:
      abort(404)

@ns_img_res.route(routing.get('namespace_image', 'image'))
class ImageResourceResource(Resource):
  """Handles multiple image resources"""
  @api_website.expect(_parser_get_images)
  @api_website.marshal_with(_image_resource_model, as_list=True)
  def get(self):
    """Returns all filtered image resources."""
    names = list(_parser_get_images.parse_args()['names'])
    return ImageResourceEntity.query.filter(ImageResourceEntity.resource.in_(names)).all()
