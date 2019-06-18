"""Base Model"""
import datetime
from .db import DB

class Base():
    """Abstract class for tables."""
    #pylint: disable=E1101
    id = DB.Column(DB.Integer, primary_key=True)
    last_updated = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow)
    created = DB.Column(DB.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return '<Base>'
