"""Media Model"""
from typing import List
from .db import DB
from .Base import Base as BaseModel

class Media(BaseModel, DB.Model):
    """media table."""

    SRC_LENGTH: List[int] = [1, 1024]
    TITLE_LENGTH: List[int] = [1, 128]
    LICENSE_LENGTH: List[int] = [1, 64]
    DESCRIPTION_LENGTH: List[int] = [0, 8192]
    #pylint: disable=E1101
    src = DB.Column(DB.String(SRC_LENGTH[1]), unique=True, nullable=False)
    title = DB.Column(DB.String(TITLE_LENGTH[1]), nullable=False)
    license = DB.Column(DB.String(LICENSE_LENGTH[1]), nullable=False)
    description = DB.Column(DB.String(DESCRIPTION_LENGTH[1]))
    width = DB.Column(DB.Integer, nullable=False)
    height = DB.Column(DB.Integer, nullable=False)
