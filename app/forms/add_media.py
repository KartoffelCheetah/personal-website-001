"""Add media parser"""

from app.models.Media import Media as MediaModel
from app.validators import length
from .base import BASE_PARSER

ADD_MEDIA_PARSER = BASE_PARSER.copy()

ADD_MEDIA_PARSER.add_argument(
    'src',
    type=length(MediaModel.SRC_LENGTH[0], MediaModel.SRC_LENGTH[1], str),
    required=True,
    location='form',
).add_argument(
    'title',
    type=length(MediaModel.TITLE_LENGTH[0], MediaModel.TITLE_LENGTH[1], str),
    required=True,
    location='form',
).add_argument(
    'license',
    type=length(MediaModel.LICENSE_LENGTH[0], MediaModel.LICENSE_LENGTH[1], str),
    required=True,
    location='form',
).add_argument(
    'description',
    type=length(MediaModel.DESCRIPTION_LENGTH[0], MediaModel.DESCRIPTION_LENGTH[1], str),
    required=False,
    location='form',
)
