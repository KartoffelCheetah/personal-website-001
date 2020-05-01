"""Entity for media elements"""
from typing import Dict
from app.models.db import DB
from .abstract_base_entity import AbstractBaseEntity

class MediaEntity(AbstractBaseEntity, DB.Model): # pylint: disable=too-few-public-methods
    """media table."""

    SRC_LENGTH: Dict[str, int] = {'min_length': 1, 'max_length': 1024}
    TITLE_LENGTH: Dict[str, int] = {'min_length': 1, 'max_length': 128}
    LICENSE_LENGTH: Dict[str, int] = {'min_length': 1, 'max_length': 64}
    DESCRIPTION_LENGTH: Dict[str, int] = {'min_length': 0, 'max_length': 8192}
    #pylint: disable=E1101
    src = DB.Column(DB.String(SRC_LENGTH['max_length']), unique=True, nullable=False)
    title = DB.Column(DB.String(TITLE_LENGTH['max_length']), nullable=False)
    license = DB.Column(DB.String(LICENSE_LENGTH['max_length']), nullable=False)
    description = DB.Column(DB.String(DESCRIPTION_LENGTH['max_length']))
    width = DB.Column(DB.Integer, nullable=False)
    height = DB.Column(DB.Integer, nullable=False)

    def __repr__(self) -> str:
        return '<MediaEntity %r>' % self.title
