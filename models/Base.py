"""Base Model"""
import datetime
from .db import db

class Base():
    """Abstract class for tables."""

    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return '<Base>'
