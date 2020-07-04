"""Abstract Base Entity"""
import datetime
from app.models.db import DB

class AbstractBaseEntity(): # pylint: disable=too-few-public-methods
    """
        Abstract entity for tables. All non abstract entities have to extend this
        entity.
    """
    #pylint: disable=E1101
    id = DB.Column(DB.Integer, primary_key=True)
    last_updated = DB.Column(DB.DateTime, onupdate=datetime.datetime.utcnow)
    created = DB.Column(DB.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return '<AbstractBaseEntity>'
