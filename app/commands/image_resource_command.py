"""Image Commands"""
import os
from flask import current_app
from flask.cli import AppGroup
from flask_sqlalchemy import sqlalchemy
from app.models.image_resource_entity import ImageResourceEntity
from app.managers.image_resource_manager import ImageProcess, get_image_resource_entity_from_fs, save_image_thumbnails_to_fs

image_cli_group = AppGroup('image')

@image_cli_group.command('status')
def status():
  """Echoes a db/fs status."""
  db_content = {i[0] for i in ImageResourceEntity.query.with_entities(ImageResourceEntity.resource).all()}

  fs_content = set(os.listdir(os.environ['FOLDER_UPLOAD']))

  missing_from_fs = db_content - fs_content

  missing_from_db = fs_content - db_content

  current_app.logger.info(f'Found items db/fs: {len(db_content)}/{len(fs_content)}')

  if missing_from_fs:
    current_app.logger.warning(f'Missing content from FS: {missing_from_fs}')

  else:
    current_app.logger.info('OK! FS is up to date.')

  if missing_from_db:
    current_app.logger.warning(f'Missing content from DB: {missing_from_db}')

  else:
    current_app.logger.info('OK! DB is up to date.')

  for conf in ImageProcess.thumb_conf:
    th_content = set(os.listdir(conf['path']))
    missing_parents = th_content - fs_content
    missing_thumbnails = fs_content - th_content

    if missing_parents:
      current_app.logger.info(f"No image for thumbnails: ({conf['path']}) | {missing_parents}")

    else:
      current_app.logger.info(f"OK! All thumbnails have parents in {conf['path']}")

    if missing_thumbnails:
      current_app.logger.info(f"No thumbnail for images: ({conf['path']}) | {missing_thumbnails}")

    else:
      current_app.logger.info(f"OK! All images have thumbnails in {conf['path']}")

@image_cli_group.command('fs2db')
def fs2db():
  """Sync filesystem to database"""
  current_app.logger.info('fs2db startup...')

  db_content = {i[0] for i in ImageResourceEntity.query.with_entities(ImageResourceEntity.resource).all()}

  fs_content = set(os.listdir(os.environ['FOLDER_UPLOAD']))

  images2sync = fs_content - db_content

  current_app.logger.info('images2sync %s' % images2sync)

  database = current_app.config['database']

  for fs_image in images2sync:
    new_media = get_image_resource_entity_from_fs(fs_image)

    database.session.add(new_media)

    save_image_thumbnails_to_fs(fs_image)

  try:
    database.session.commit()

  except sqlalchemy.exc.IntegrityError:
    current_app.logger.exception('Integrity error in db.')

  current_app.logger.info('...fs2db ends')
