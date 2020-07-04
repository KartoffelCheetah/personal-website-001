"""Entity for media elements"""
from app.models.db import DB
from .abstract_resource_entity import AbstractResourceEntity

class ImageResourceEntity(AbstractResourceEntity, DB.Model): # pylint: disable=too-few-public-methods
    """Specialized resource entity with image metadata storage."""
    #pylint: disable=E1101
    width = DB.Column(DB.Integer, nullable=False)
    height = DB.Column(DB.Integer, nullable=False)

    def __repr__(self) -> str:
        return '<ImageResourceEntity %rx%r : %r>' % (self.width, self.height, self.resource)
