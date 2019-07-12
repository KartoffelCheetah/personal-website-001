"""Add media parser"""

from marshmallow import Schema, fields, post_load, validate
from flask_restplus import fields as frpf
from app.models.api import API
from app.models.Media import Media as MediaModel

MEDIA_DOC = API.model('Media', {
    'src': frpf.String(required=True, description='Image source, should be unique.'),
    'title': frpf.String(required=True),
    'license': frpf.String(required=True),
    'description': frpf.String(required=False),
})

class MediaSchema(Schema):
    src = fields.String(
        required=True,
        validate=[
            validate.Length(**MediaModel.SRC_LENGTH)
        ]
    )
    title = fields.String(
        required=True,
        validate=[
            validate.Length(**MediaModel.TITLE_LENGTH)
        ]
    )
    license = fields.String(
        required=True,
        validate=[
            validate.Length(**MediaModel.LICENSE_LENGTH)
        ]
    )
    description = fields.String(
        required=False,
        validate=[
            validate.Length(**MediaModel.DESCRIPTION_LENGTH)
        ]
    )

    @post_load
    def create_media(self, data):
        # TODO: compute dimensions
        return MediaModel(**data, width=0, height=0)
