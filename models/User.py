from .db import db
from passlib.hash import pbkdf2_sha512
from itsdangerous import (
    TimedJSONWebSignatureSerializer as TJWSSerializer,
    BadSignature,
    SignatureExpired)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def generate_auth_token(self, secret_key, expiration=600):
        """Generates a token for authorization."""
        s = TJWSSerializer(secret_key, expires_in=expiration)
        return s.dumps({ 'id':self.id })

    @staticmethod
    def verify_auth_token(secret_key, token):
        """Verifies if token is eligible for authentication."""
        s = TJWSSerializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token but expired
        except BadSignature:
            return None # invalid token
        user = User.query.filter_by(id=data['id']).first()
        # if there is no such user in db, then user is None
        return user

    def verify_password_hash(self, password):
        return pbkdf2_sha512.verify(password, self.password_hash)

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha512.hash(password)
