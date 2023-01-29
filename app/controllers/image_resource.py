#pylint: disable=R0201
"""Image Resource Controller"""
from urllib.parse import urljoin
from flask import current_app, url_for, abort, request
from flask_restx import Resource, fields
from app.models.image_resource_entity import ImageResourceEntity
from app.definitions import routing
from app.models.api import api_website
from app.managers.image_resource_manager import ImageMetaData, get_thumbnail_conf_by_thid

ns_img_res = api_website.namespace(
	routing.get('namespace_image', 'namespace'),
	description='Image resource management',
)

def create_image_resource_model(thumbnail_levels):
	return api_website.model(f'ImageResource{thumbnail_levels}', {
		'@context': fields.String('https://schema.org', example='https://schema.org'),
		'@type': fields.String('ImageObject', example='ImageObject'),
		'@id': fields.String(
			attribute=lambda imd: urljoin(request.host_url, url_for(
				'api.image_image_resource_resource_by_resource',
				thid=imd.thid,
				name=imd.filename,
			)),
			example='/api/image/hello-example.png',
		),
		'name': fields.String(attribute='filename'),
		'contentUrl': fields.String(
			attribute=lambda imd: urljoin(request.host_url, str(imd.relative_url)),
			example='hello-example.png',
			**ImageResourceEntity.RI_LENGTH,
		),
		'thumbnail': fields.List(
			fields.Nested(create_image_resource_model(thumbnail_levels - 1)) if thumbnail_levels > 0 else fields.Raw(),
			attribute=lambda imd: [t for t in imd.children_image_meta_data],
		),
		'height': fields.Integer(),
		'width': fields.Integer()
	})

_image_resource_model = create_image_resource_model(thumbnail_levels=1)

_parser_get_images = api_website.parser()
_parser_get_images.add_argument('names', type=str, action='append', required=True)
_parser_get_images.add_argument('thid', type=str, required=True)

@ns_img_res.route(routing.get('namespace_image', 'image')+'<thid>/<name>')
class ImageResourceResourceByResource(Resource):
	"""Handles a single image resource"""
	@api_website.marshal_with(_image_resource_model, as_list=False)
	def get(self, thid, name):
		"""Returns an image resource."""
		ire = ImageResourceEntity.query.filter_by(resource=name).first()
		conf = get_thumbnail_conf_by_thid(thid)
		if conf:
			imd = ImageMetaData(filename=ire.resource, thumbnail_conf=conf, original_width=ire.width, original_height=ire.height)
			if imd:
				return imd
		abort(404)

@ns_img_res.route(routing.get('namespace_image', 'image'))
class ImageResourceResource(Resource):
	"""Handles multiple image resources"""
	@api_website.expect(_parser_get_images)
	@api_website.marshal_with(_image_resource_model, as_list=True)
	def get(self):
		"""Returns all filtered image resources."""
		names = list(_parser_get_images.parse_args()['names'])
		thid = _parser_get_images.parse_args()['thid']
		conf = get_thumbnail_conf_by_thid(thid)
		if conf:
			ires = ImageResourceEntity.query.filter(ImageResourceEntity.resource.in_(names)).all()
			imds = list(map(lambda ire: ImageMetaData(filename=ire.resource, thumbnail_conf=conf, original_width=ire.width, original_height=ire.height), ires))
			return imds
		abort(404)
