"""Image Resource Manager"""
import os
from pathlib import Path
from typing import Final, Callable
from logging import Logger
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import current_app
from PIL import Image
from app.models.image_resource_entity import ImageResourceEntity

class ImageProcess:

  thumb_conf: Final[list] = [
    {
      'size': lambda s: (s[0]//4, s[1]//4),
      'path': os.environ['FOLDER_UPLOAD_25'],
    },
    {
      'size': lambda s: (s[0]//2, s[1]//2),
      'path': os.environ['FOLDER_UPLOAD_50'],
    },
  ]

  def __init__(self, unsafe_name, path=os.environ['FOLDER_UPLOAD'], size=lambda s: s):
    self.name: str = get_securefname(unsafe_name)
    self.fpath: str = os.path.join(path, self.name)
    self.size: Callable = size
    self.url: Path = Path(current_app.static_url_path)/Path(self.fpath).resolve().relative_to(current_app.static_folder)
    if path == os.environ['FOLDER_UPLOAD']:
      self.thumbnails: list = [ImageProcess(self.name, **conf) for conf in self.thumb_conf]

def get_securefname(filename: str) -> str:
  """Returns a filename which is safe to use. Currently uses werkzeug's
  implementation."""
  return secure_filename(filename)

def is_conflicting(filename: str, logger: Logger) -> bool:
  """Returns true if image is in db or in fs"""
  ipr = ImageProcess(filename)

  if ImageResourceEntity.query.filter_by(resource=ipr.name).first():
    logger.exception('Post image resource - image already exists in db.')
    return True

  if os.path.exists(ipr.fpath):
    logger.exception('Post image resource - image already exists in fs.')
    return True

  return False

def save_image_thubnails_to_fs(filename: str) -> None:
  """Generates the thumbnails for an image already existing on the fs."""

  ipr = ImageProcess(filename)
  image = Image.open(ipr.fpath)

  for child_ipr in ipr.thumbnails:
    thumbnail_image = image.copy()
    thumbnail_image.thumbnail(child_ipr.size(image.size))
    thumbnail_image.save(child_ipr.fpath)

def save_image_resource_to_fs(filename: str, imagedata: FileStorage) -> None:
  """Saves image to fs."""
  ipr = ImageProcess(filename)
  imagedata.save(ipr.fpath)
  save_image_thubnails_to_fs(ipr.name)

def get_image_resource_entity_from_fs(filename: str) -> ImageResourceEntity:
  """Returns a corresponding ImageResourceEntity.
  Database commit required."""
  ipr = ImageProcess(filename)
  width, height = Image.open(ipr.fpath).size
  return ImageResourceEntity(resource=ipr.name, width=width, height=height)
