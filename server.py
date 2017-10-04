#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from flask import Flask, render_template, url_for, g, abort, redirect
import os, pathlib, base64
from os.path import splitext
import sqlite3
import db # cant be from db import something because of circular import

app = Flask(__name__)
DATABASE = 'imagedb.db'
PHOTOS = 'img/photos/'
DRAWINGS = 'img/drawings/'
LOGOS = 'img/logos/'
THUMBNAILS = PHOTOS+'_thumbnails/'
THUMBNAILS_DR = DRAWINGS+'_thumbnails/'
IMGEXT = ['jpg', 'jpeg', 'png', 'svg', 'gif']
IMGEXT = tuple(list(map( lambda x:x.upper(), IMGEXT))+IMGEXT)
#////////////////////////////////////

## ROUTES ##
# -----------------------------------------------
@app.route('/')#---------------------------------
def index():
    # return render_template('index.html.j2')
    return redirect('/about')
#------------------------------------------------
@app.route('/contact')#--------------------------
def contact():
    return render_template('contact.html.j2')
#------------------------------------------------
@app.route('/faq')#------------------------------
def faq():
    return render_template('faq.html.j2')
#------------------------------------------------
@app.route('/artgallery/')#-------------------------
def artgallery():
    try:
        conn = get_db()
        c = conn.cursor()
        phs = db.select_all_drawing_thumbnail(c)
        phs = [[url.split(DRAWINGS, maxsplit=1)[1],title] for url,title in phs]
    except Exception as e:
        print('\x1b[31m', e, '\x1b[0m')
        abort(500)
    finally:
        c.close()
        conn.close()
    return render_template('artgallery.html.j2', photos=phs,THUMBNAILS=THUMBNAILS_DR)
#------------------------------------------------
@app.route('/photogallery/')#---------------------------
def photogallery():
    try:
        conn = get_db()
        c = conn.cursor()
        phs = db.select_all_photo_thumbnail(c)
        phs = [[url.split(PHOTOS, maxsplit=1)[1],title] for url,title in phs]
    except Exception as e:
        print('\x1b[31m', e, '\x1b[0m')
        abort(500)
    finally:
        c.close()
        conn.close()
    return render_template('photogallery.html.j2', photos=phs,THUMBNAILS=THUMBNAILS)
#------------------------------------------------
@app.route('/about')#----------------------------
def about():
    logos = getLogos()
    return render_template('about.html.j2', techs=logos)
#------------------------------------------------
#------------------------------------------------
@app.route('/photos/<folder>/<img>')#----------------------------
def photos(folder, img):
    # security?
    imgUrl = '/{}{}/{}'.format(PHOTOS, folder, img)
    try:
        conn = get_db()
        c = conn.cursor()
        img = db.select_a_photo(c, imgUrl) #mainPhoto
        phs = db.select_all_photo_thumbnail(c)
        phs = calc_neighbours(phs, img, 2, func=lambda x: x[0])
        phs = [[url.split(PHOTOS, maxsplit=1)[1],title] for url,title in phs]
    except Exception as e:
        print('\x1b[31m', e, '\x1b[0m')
        abort(500)
    finally:
        c.close()
        conn.close()
    return render_template('photos.html.j2', img=img, photos=phs,THUMBNAILS=THUMBNAILS)
#------------------------------------------------
@app.route('/drawings/<img>')#----------------------------
def drawings(img):
    # security?
    imgUrl = '/{}{}'.format(DRAWINGS, img)
    try:
        conn = get_db()
        c = conn.cursor()
        img = db.select_a_drawing(c, imgUrl) #mainPhoto
        phs = db.select_all_drawing_thumbnail(c)
        phs = calc_neighbours(phs, img, 2, func=lambda x: x[0])
        phs = [[url.split(DRAWINGS, maxsplit=1)[1],title] for url,title in phs]
    except Exception as e:
        print('\x1b[31m', e, '\x1b[0m')
        abort(500)
    finally:
        c.close()
        conn.close()
    return render_template('drawings.html.j2', img=img, photos=phs,THUMBNAILS=THUMBNAILS_DR)
#------------------------------------------------

#ERRORHANDLER------------------------------------
@app.errorhandler(500)#--------------------------
def internal_server_error(err):
    print('\x1b[31m', err, '\x1b[0m') # TODO log it somewhere
    return app.send_static_file('html/500.html'), 500
@app.errorhandler(404)
def not_found(err):
    return render_template('404.html.j2'), 404
#------------------------------------------------

def getLogos():
    logos = os.listdir(app.static_folder + '/'+ LOGOS)
    logos = [logo for logo in logos if logo.endswith(IMGEXT)]
    return [{
                'name':splitext(logo)[0],
                'link':pathlib.Path(app.static_folder+ '/' + LOGOS+splitext(logo)[0]+'.txt').read_text(),
                'filename':logo
            } for logo in logos]

def calc_neighbours(ofItems, targetItem, n, func=lambda x:x):
    """Search through ofItems for targetItem.
    Returns n number of neighbours of targetItem from ofItems."""
    for i in range(len(ofItems)):
        if func(ofItems[i])==func(targetItem):
            break # we found our target index
    # get the neighbours, handle edge cases
    return ofItems[max(0,i-n):min(i+n+1,len(ofItems))]

def get_db():
    """Returns an sqlite3.Connection object stored in g.
    Or creates it if doesn't exist yet."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#////////////////////////////////////
if __name__=='__main__':
    app.run(
        debug=True,
        threaded=True
    )
