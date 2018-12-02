from .db import db

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    src = db.Column(db.String(1024), unique=True, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    license = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(4096))
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
