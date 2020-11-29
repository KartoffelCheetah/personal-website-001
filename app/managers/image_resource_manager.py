"""Image Resource Manager"""
import os
from logging import Logger
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from PIL import Image
from app.models.image_resource_entity import ImageResourceEntity

def get_securefname(filename):
    """Returns a filename which is safe to use. Currently uses werkzeug's
    implementation."""
    return secure_filename(filename)

def get_securefpath(securefname: str) -> str:
    """Returns the path to the file."""
    return os.path.join(os.environ['FOLDER_UPLOAD'], securefname)

def is_exists_in_db(securefname: str, logger: Logger) -> bool:
    """Returns if db already contains image."""
    if ImageResourceEntity.query.filter_by(resource=securefname).first():
        logger.exception('Post image resource - image already exists in db.')
        return True
    return False

def is_exists_in_fs(securefname: str, logger: Logger) -> bool:
    """Returns if fs already contains image."""
    if os.path.exists(get_securefpath(securefname)):
        logger.exception('Post image resource - image already exists in fs.')
        return True
    return False

def save_image_resource_to_fs(securefname: str, imagedata: FileStorage) -> None:
    """Saves image to fs."""
    securefpath = get_securefpath(securefname)
    imagedata.save(securefpath)

def get_image_resource_entity_from_fs(securefname: str) -> ImageResourceEntity:
    """Returns a corresponding ImageResourceEntity.
    Database commit required."""
    securefpath = get_securefpath(securefname)
    width, height = Image.open(securefpath).size
    return ImageResourceEntity(resource=securefname, width=width, height=height)

