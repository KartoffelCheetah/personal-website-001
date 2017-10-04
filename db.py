#! /usr/bin/python3

import sqlite3
from PIL import Image
import io
from server import app, DATABASE, PHOTOS, DRAWINGS, THUMBNAILS, THUMBNAILS_DR # Flask app, database

"""This program creates the photos- and drawings Cursor objects,
contains the basic functions to operate the SQLite db.
It's separate from database_operations, which use this module through the main module's interface."""


# create/connect db, # autocommit
# ---------------------------------------------------
imagedb = sqlite3.connect(DATABASE)
photos, drawings = imagedb.cursor(), imagedb.cursor()
photos.connection.isolation_level, drawings.connection.isolation_level = None, None
# ---------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------
def orientate(image):
    """Rotates an image based on it's Orientation exif tag"""
    orientation = image._getexif()[274]
    if orientation == 3 :
        image = image.rotate(180, expand=True)
    elif orientation == 6 :
        image = image.rotate(270, expand=True)
    elif orientation == 8 :
        image = image.rotate(90, expand=True)
    return image
def create_thumbnail(image, url):
    """Creates thumbnail, be aware
    it uses the original image for creation"""
    image.thumbnail((200,200))
    new_url = '{}/{}{}'.format(
        app.static_folder,
        THUMBNAILS,
        url.split(PHOTOS, maxsplit=1)[1]
    )
    image.save(new_url, format='JPEG', resample=Image.ANTIALIAS)
def create_thumbnail_DR(image, url):
    """Creates thumbnail, be aware
    it uses the original image for creation"""
    image.thumbnail((200,200))
    new_url = '{}/{}{}'.format(
        app.static_folder,
        THUMBNAILS_DR,
        url.split(DRAWINGS, maxsplit=1)[1]
    )
    image.save(new_url, format='PNG', resample=Image.ANTIALIAS)
# ---------------------------------------------------
# DB FUNCTIONS
# ---------------------------------------------------
def create_db():
    """Creates the tables"""
    photos.execute("""
    CREATE TABLE IF NOT EXISTS photos
        (id INTEGER PRIMARY KEY,
        url TEXT UNIQUE,
        title TEXT,
        description TEXT,
        datetimeoriginal TEXT,
        uploaddate TEXT DEFAULT CURRENT_TIMESTAMP,
        license TEXT DEFAULT 'All rights reserved'
        )""")
    drawings.execute("""
    CREATE TABLE IF NOT EXISTS drawings
        (id INTEGER PRIMARY KEY,
        url TEXT UNIQUE,
        title TEXT,
        description TEXT,
        datetimeoriginal TEXT,
        uploaddate TEXT DEFAULT CURRENT_TIMESTAMP,
        license TEXT DEFAULT 'All rights reserved'
        )""")
# ---------------------------------------------------
# PHOTOS
# ---------------------------------------------------
def insert_photo(url, title, desc, license=None):
    """Inserts drawing into the database"""
    image = Image.open(app.static_folder + url)
    datetimeoriginal = image._getexif()[36867]
    image = orientate(image)
    create_thumbnail(image, url)
    if license:
        drawings.execute("""
        INSERT INTO photos
        (url, description, datetimeoriginal, title, license) VALUES (?,?,?,?,?)
        """, (url, desc, datetimeoriginal, title, license))
    else:
        drawings.execute("""
        INSERT INTO photos
        (url, description, datetimeoriginal, title) VALUES (?,?,?,?)
        """, (url, desc, datetimeoriginal, title))
# ---------------------------------------------------
# def select_all_photo(session):
#     """Get a list of all images from db"""
#     session.execute("""
#     SELECT url, description, datetimeoriginal,
#            uploaddate, title FROM photos
#     """)
#     return session.fetchall()
# ---------------------------------------------------
def select_all_photo_thumbnail(session):
    """Get a list of all image thumbnails from db"""
    session.execute("""
    SELECT url, title FROM photos
    """)
    return session.fetchall()
# ---------------------------------------------------
def select_a_photo(session, url):
    """Get a single image from db"""
    session.execute("""
    SELECT url, description, datetimeoriginal,
           uploaddate, license, title FROM photos
           WHERE url = ? LIMIT 1
    """, (url,))
    return session.fetchone()
# ---------------------------------------------------
# DRAWINGS
# ---------------------------------------------------
def insert_drawing(url, title, desc, createDate, license=None):
    """Inserts drawing into the database"""
    image = Image.open(app.static_folder + url)
    # datetimeoriginal = image._getexif()[36867]
    datetimeoriginal = createDate
    # image = orientate(image)
    create_thumbnail_DR(image, url)
    if license:
        drawings.execute("""
        INSERT INTO drawings
        (url, description, datetimeoriginal, title, license) VALUES (?,?,?,?,?)
        """, (url, desc, datetimeoriginal, title, license))
    else:
        drawings.execute("""
        INSERT INTO drawings
        (url, description, datetimeoriginal, title) VALUES (?,?,?,?)
        """, (url, desc, datetimeoriginal, title))
# ---------------------------------------------------
# def select_all_drawing(session):
#     """Get a list of all images from db"""
#     session.execute("""
#     SELECT url, description, datetimeoriginal,
#            uploaddate, title FROM drawings
#     """)
#     return session.fetchall()
# ---------------------------------------------------
def select_all_drawing_thumbnail(session):
    """Get a list of all image thumbnails from db"""
    session.execute("""
    SELECT url, title FROM drawings
    """)
    return session.fetchall()
# ---------------------------------------------------
def select_a_drawing(session, url):
    """Get a single image from db"""
    session.execute("""
    SELECT url, description, datetimeoriginal,
           uploaddate, license, title FROM drawings
           WHERE url = ? LIMIT 1
    """, (url,))
    return session.fetchone()
# ---------------------------------------------------
