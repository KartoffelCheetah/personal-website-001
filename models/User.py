from .db import db
from passlib.hash import pbkdf2_sha512
# User class has to implement flask_login's UserMixin
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def verify_password_hash(self, password):
        return pbkdf2_sha512.verify(password, self.password_hash)

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha512.hash(password)
