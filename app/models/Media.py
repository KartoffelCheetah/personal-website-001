"""Media Model"""
from typing import Dict
from app.models.db import DB
from .Base import Base as BaseModel

class Media(BaseModel, DB.Model):
    """media table."""

    SRC_LENGTH: Dict[str, int] = {'min': 1, 'max': 1024}
    TITLE_LENGTH: Dict[str, int] = {'min': 1, 'max': 128}
    LICENSE_LENGTH: Dict[str, int] = {'min': 1, 'max': 64}
    DESCRIPTION_LENGTH: Dict[str, int] = {'min': 0, 'max': 8192}
    #pylint: disable=E1101
    src = DB.Column(DB.String(SRC_LENGTH['max']), unique=True, nullable=False)
    title = DB.Column(DB.String(TITLE_LENGTH['max']), nullable=False)
    license = DB.Column(DB.String(LICENSE_LENGTH['max']), nullable=False)
    description = DB.Column(DB.String(DESCRIPTION_LENGTH['max']))
    width = DB.Column(DB.Integer, nullable=False)
    height = DB.Column(DB.Integer, nullable=False)
