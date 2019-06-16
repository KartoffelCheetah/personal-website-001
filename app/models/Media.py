"""Media Model"""
from . import DB
from .Base import Base as BaseModel

class Media(BaseModel, DB.Model):
    """media table."""
    src = DB.Column(DB.String(1024), unique=True, nullable=False)
    title = DB.Column(DB.String(128), nullable=False)
    license = DB.Column(DB.String(64), nullable=False)
    description = DB.Column(DB.String(8192))
    width = DB.Column(DB.Integer, nullable=False)
    height = DB.Column(DB.Integer, nullable=False)
