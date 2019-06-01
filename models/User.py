from .db import db
from passlib.hash import pbkdf2_sha512
from dotenv import load_dotenv, find_dotenv
import os
# timing is handled by session so
# TimedJSONWebSignatureSerializer is not needed
from itsdangerous import (
    BadSignature,
    SignatureExpired,
    JSONWebSignatureSerializer as Serializer)
# User class has to implement flask_login's UserMixin
from flask_login import UserMixin

load_dotenv(dotenv_path=find_dotenv('.env.server'))

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
        """Expects plain text pwd and returns hashed variant"""
        return pbkdf2_sha512.hash(password)

    def get_id(self):
        """Overwrites FlaskLogin method.
        Using the hash of the password to authenticate.
        Whenever pwd changes the pwdCheck wont be readable."""
        serializer = Serializer(
            os.getenv('SECRET_KEY'),
            salt=self.password_hash)
        # wont validate after pwd is changed
        pwdCheck = serializer.dumps(self.id)

        return '{}->{}'.format(self.id, pwdCheck.decode())

    def session_auth(self, pwdCheck):
        """Checks if user pwd changed since login"""
        serializer = Serializer(
            os.getenv('SECRET_KEY'),
            salt=self.password_hash)
        try:
            return serializer.loads(pwdCheck.encode()) == self.id
        except (BadSignature, SignatureExpired, UnicodeError):
            #NOTE: I know we do not use signature expired,
            #NOTE: as we do not use timed token.
            #NOTE: Leaving this here for possible future changes.
            return None
