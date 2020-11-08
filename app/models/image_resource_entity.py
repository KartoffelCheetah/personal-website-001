"""Entity for media elements"""
from app.models.db import db
from .abstract_resource_entity import AbstractResourceEntity

class ImageResourceEntity(AbstractResourceEntity, db.Model): # pylint: disable=too-few-public-methods
    """Specialized resource entity with image metadata storage."""
    #pylint: disable=E1101
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return '<ImageResourceEntity %rx%r : %r>' % (self.width, self.height, self.resource)
