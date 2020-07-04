"""Entity for blog elements"""
from app.models.db import DB
from .abstract_resource_entity import AbstractResourceEntity

class BlogResourceEntity(AbstractResourceEntity, DB.Model): #pylint: disable=too-few-public-methods
    """Resource entity for blogs."""

    def __repr__(self) -> str:
        return '<BlogResourceEntity %r>' % self.created
