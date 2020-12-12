"""Image Resource Manager"""
import os
from typing import Final
from logging import Logger
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from PIL import Image
from app.models.image_resource_entity import ImageResourceEntity

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

def get_securefname(filename: str) -> str:
    """Returns a filename which is safe to use. Currently uses werkzeug's
    implementation."""
    return secure_filename(filename)

def _get_securefpath(filename: str) -> str:
    """Returns the path to the file."""
    return os.path.join(os.environ['FOLDER_UPLOAD'], get_securefname(filename))

def is_conflicting(filename: str, logger: Logger) -> bool:

    if ImageResourceEntity.query.filter_by(resource=get_securefname(filename)).first():
        logger.exception('Post image resource - image already exists in db.')
        return True

    if os.path.exists(_get_securefpath(filename)):
        logger.exception('Post image resource - image already exists in fs.')
        return True

    return False

def save_image_thubnails_to_fs(filename: str) -> None:
    """Generates the thumbnails for an image already existing on the fs."""

    securefpath = _get_securefpath(filename)
    image = Image.open(securefpath)

    for conf in thumb_conf:
        thumbnail_image = image.copy()
        thumbnail_image.thumbnail(conf['size'](image.size))
        thumb_filename = get_securefname(os.path.split(image.filename)[1])
        thumbnail_image.save(os.path.join(conf['path'], thumb_filename))

def save_image_resource_to_fs(filename: str, imagedata: FileStorage) -> None:
    """Saves image to fs."""
    securefpath = _get_securefpath(filename)
    imagedata.save(securefpath)
    save_image_thubnails_to_fs(filename)

def get_image_resource_entity_from_fs(filename: str) -> ImageResourceEntity:
    """Returns a corresponding ImageResourceEntity.
    Database commit required."""
    securefname = get_securefname(filename)
    securefpath = _get_securefpath(securefname)
    width, height = Image.open(securefpath).size
    return ImageResourceEntity(resource=securefname, width=width, height=height)

