#!.venv/bin/python3

import sqlite3
import io, os
from os.path import join as pathJoin
from IMfunctions import *
from server import app, DATABASE, PHOTOS, DRAWINGS, THUMBNAILS, STAGING_AREA, FULL_THUMBNAILS, FULL_IMAGES # Flask app, database

"""This program creates the photos- and drawings Cursor objects,
contains the basic functions to operate the SQLite db.
Use this module through the main module's interface or from the server itself."""


# create/connect db, # autocommit
# ---------------------------------------------------
imagedb = sqlite3.connect(DATABASE)
photos, drawings = imagedb.cursor(), imagedb.cursor()
photos.connection.isolation_level, drawings.connection.isolation_level = None, None
# ---------------------------------------------------
# ---------------------------------------------------
imagedbDict = sqlite3.connect(DATABASE)
imagedbDict.row_factory = sqlite3.Row
photosDict, drawingsDict = imagedbDict.cursor(), imagedbDict.cursor()
photosDict.connection.isolation_level, drawingsDict.connection.isolation_level = None, None


DEFAULTPHOTOLICENSE = "All rights reserved"
DEFAULTDRAWINGLICENSE = "All rights reserved"
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
        license TEXT DEFAULT '%s',
        xres INTEGER,
        yres INTEGER
        )""" % DEFAULTPHOTOLICENSE)
    drawings.execute("""
    CREATE TABLE IF NOT EXISTS drawings
        (id INTEGER PRIMARY KEY,
        url TEXT UNIQUE,
        title TEXT,
        description TEXT,
        datetimeoriginal TEXT,
        uploaddate TEXT DEFAULT CURRENT_TIMESTAMP,
        license TEXT DEFAULT '%s',
        xres INTEGER,
        yres INTEGER
        )""" % DEFAULTDRAWINGLICENSE)
# ---------------------------------------------------
# GENERIC
# ---------------------------------------------------
def getDefault(tableName, colName) :
    """Specify a table's column and the function returns it's default value."""
    cols = photosDict.execute("PRAGMA table_info('%s')" % tableName)
    for col in cols :
        if col['name'] == colName :
            return col['dflt_value']
    raise sqlite3.OperationalError('no such column: %s' % colName)
# ---------------------------------------------------
def print_table(selected_table):
    """Receives a list of sqlite3.Row objects and print all of them to stdout"""
    yellow = '\x1b[33m'
    normal = '\x1b[0m'
    magenta = '\x1b[35m'
    for row in selected_table:
        print('-------------')
        for k,v in zip(row.keys(), row):
            print(yellow+str(k)+': '+magenta+str(v)+normal)
# ---------------------------------------------------
def dict_from_row(row):
    """Transforms an sqlite3.Row object to a dictionary"""
    if type(row)==sqlite3.Row :
        return dict(zip(row.keys(), row))
    else :
        return [dict(zip(r.keys(), r)) for r in row]
# ---------------------------------------------------
# ---------------------------------------------------
# PHOTOS
# ---------------------------------------------------
def insert_photo(url, title, desc, createDate, license=None, **kwargs):
    """Inserts drawing into the database"""
    if not license :
        license = DEFAULTPHOTOLICENSE
    # base image location
    staged_url = pathJoin(STAGING_AREA,PHOTOS,url)
    # thumbnail image location
    thumb_url = pathJoin(FULL_THUMBNAILS,PHOTOS,url)
    # public image location
    public_url = pathJoin(FULL_IMAGES,PHOTOS,url)
    # temporary thumbnail image location
    temp_thumb_url = thumb_url + '_tmp'
    # temporary image location
    temp_url = public_url + '_tmp'

    createThumbnail(staged_url, temp_thumb_url)
    createRotatedImage(staged_url, temp_url)
    xres, yres = getDimensions(temp_url)
    drawings.execute("""
    INSERT INTO photos
    (url, description, datetimeoriginal, title, license, xres, yres) VALUES (?,?,?,?,?,?,?)
    """, (url, desc, createDate, title, license, xres, yres))
# ---------------------------------------------------
def select_all_photos(session):
    """Get a list of all images from db"""
    session.execute("""
    SELECT * FROM photos
    """)
    return session.fetchall()
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
           uploaddate, license, title, xres, yres FROM photos
           WHERE url = ? LIMIT 1
    """, (url,))
    return session.fetchone()
# ---------------------------------------------------
# ---------------------------------------------------
# DRAWINGS
# ---------------------------------------------------
def insert_drawing(url, title, desc, createDate, license=None, **kwargs):
    """Inserts drawing into the database"""
    if not license :
        license = DEFAULTDRAWINGLICENSE
    # base image location
    staged_url = pathJoin(STAGING_AREA,DRAWINGS,url)
    # thumbnail image location
    thumb_url = pathJoin(FULL_THUMBNAILS,DRAWINGS,url)
    # public image location
    public_url = pathJoin(FULL_IMAGES,DRAWINGS,url)
    # temporary thumbnail image location
    temp_thumb_url = thumb_url + '_tmp'
    # temporary image location
    temp_url = public_url + '_tmp'

    createThumbnail(staged_url, temp_thumb_url)
    createRotatedImage(staged_url, temp_url)
    xres, yres = getDimensions(temp_url)
    drawings.execute("""
    INSERT INTO drawings
    (url, description, datetimeoriginal, title, license, xres, yres) VALUES (?,?,?,?,?,?,?)
    """, (url, desc, createDate, title, license, xres, yres))
# ---------------------------------------------------
def select_all_drawings(session):
    """Get a list of all images from db"""
    session.execute("""
    SELECT * FROM drawings
    """)
    return session.fetchall()
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
           uploaddate, license, title, xres, yres FROM drawings
           WHERE url = ? LIMIT 1
    """, (url,))
    return session.fetchone()
# ---------------------------------------------------
