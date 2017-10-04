#! /usr/bin/python3

from db import drawings, insert_drawing

drawings.execute('BEGIN')
# DRAWINGS------------------

insert_drawing(
    '/img/drawings/wolf003_002.png',
    'Quick Wolf sketch',
    "Wuf.",
    "2017:09:19",
    "CC0"
)
insert_drawing(
    '/img/drawings/wolf004_001.png',
    'Head practice',
    "Practicing to make a head.",
    "2017:09:22",
    "CC0"
)
drawings.execute('COMMIT')
