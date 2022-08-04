"""Abstract Resource Entity"""
from typing import Dict
from app.models.abstract_base_entity import AbstractBaseEntity
from app.models.db import db

class AbstractResourceEntity(AbstractBaseEntity): #pylint: disable=too-few-public-methods
  """
    Abstract entity for resource entities. Contains a `resource identifier`
    which can be used to generate a URI and locate the resource in the file system/web.
  """
  #pylint: disable=E1101
  RI_LENGTH: Dict[str, int] = {'min_length': 1, 'max_length': 1024}
  resource = db.Column(db.String(RI_LENGTH['max_length']), nullable=False, unique=True)

  def __repr__(self) -> str:
    return '<AbstractResourceEntity>'
