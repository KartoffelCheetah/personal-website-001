"""Abstract Base Entity"""
import datetime
from app.models.db import db

class AbstractBaseEntity(): # pylint: disable=too-few-public-methods
    """
        Abstract entity for tables. All non abstract entities have to extend this
        entity.
    """
    #pylint: disable=E1101
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return '<AbstractBaseEntity>'
