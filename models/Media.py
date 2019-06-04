"""Media Model"""
from .db import db
from .Base import Base as BaseModel

class Media(BaseModel, db.Model):
    """media table."""
    src = db.Column(db.String(1024), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    license = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(8192))
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
