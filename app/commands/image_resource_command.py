"""Image Commands"""
import os
from time import sleep
from flask import current_app
from flask.cli import AppGroup
from flask_sqlalchemy import sqlalchemy
from app.models.image_resource_entity import ImageResourceEntity
from app.managers.image_resource_manager import get_image_resource_entity_from_fs

image_cli_group = AppGroup('image')

@image_cli_group.command('fs2db')
def fs2db():
    """Sync filesystem to database"""
    current_app.logger.info('fs2db startup...')

    db_content = {i.resource for i in ImageResourceEntity.query.all()}

    fs_content = os.listdir(os.environ['FOLDER_UPLOAD'])

    images2sync = {fs_image for fs_image in fs_content if fs_image not in db_content}

    images2sync_len = len(images2sync)

    if images2sync_len < 10:
        current_app.logger.info('images2sync %s' % images2sync)

    else:
        current_app.logger.info('images2sync %s number' % images2sync_len)

    database = current_app.config['database']

    for fs_image in images2sync:
        new_media = get_image_resource_entity_from_fs(fs_image)

        database.session.add(new_media)

    try:
        database.session.commit()

    except sqlalchemy.exc.IntegrityError:
        current_app.logger.exception('Integrity error in db.')

    current_app.logger.info('...fs2db ends')
