#! /usr/bin/python3

from db import photos, insert_photo

photos.execute('BEGIN')
# NAPOLI------------------
insert_photo(
    '/img/photos/Napoli/IMG_6487.JPG',
    'Empty eyes',
    "In the Museo Archeologico Nazionale di Napoli (MANN). Empty eyes. The lighting helped a lot in this image.",
    'CC0'
)
insert_photo(
    '/img/photos/Napoli/IMG_6489.JPG',
    'Deer',
    "In the Museo Archeologico Nazionale di Napoli (MANN). Deer.",
    'CC0'
)
# ------------------
# ORVIETO------------------
insert_photo(
    '/img/photos/Orvieto/IMG_6927.JPG',
    'The Belltower',
    "Streets of Orvieto. Clock and bell.",
    'CC0'
)
insert_photo(
    '/img/photos/Orvieto/IMG_6941.JPG',
    'Tufa walls',
    "Streets of Orvieto.",
    'CC0'
)
photos.execute('COMMIT')
