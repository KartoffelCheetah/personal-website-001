"""User Model"""

import os
from typing import Union
from passlib.hash import pbkdf2_sha512
from dotenv import load_dotenv, find_dotenv
# timing is handled by session so
# TimedJSONWebSignatureSerializer is not needed
from itsdangerous import (
    BadSignature,
    SignatureExpired,
    JSONWebSignatureSerializer as Serializer)
# User class has to implement flask_login's UserMixin
from flask_login import UserMixin
from .db import db
from .Base import Base as BaseModel

load_dotenv(dotenv_path=find_dotenv('.env.server'))

class User(BaseModel, UserMixin, db.Model):
    """user table"""
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __repr__(self) -> str:
        return '<User %r>' % self.username

    def verify_password_hash(self, password: str) -> bool:
        """Returns if the password is correct.

        Parameters
        ----------
        password : str
            Password of user.

        Returns
        -------
        bool
            Is password correct?

        """
        return pbkdf2_sha512.verify(password, self.password_hash)

    @staticmethod
    def hash_password(password: str) -> str:
        """Calculates password hash from plain text password.

        Parameters
        ----------
        password : str
            Password of user.

        Returns
        -------
        str
            Hashed password.

        """
        return pbkdf2_sha512.hash(password)

    def get_id(self) -> str:
        """Implements UserMixin's get_id method.
        Uses the hash of the password and the secret_key to authenticate.
        Whenever password or secret_key changes the data will be unreadable.

        Parameters
        ----------


        Returns
        -------
        str
            Identifier for user.

        """

        serializer = Serializer(
            os.getenv('SECRET_KEY'),
            salt=self.password_hash)
        # wont validate after pwd is changed
        pwd_check = serializer.dumps(self.id)

        return '{}->{}'.format(self.id, pwd_check.decode())

    def session_auth(self, pwd_check: str) -> Union[bool, None]:
        """Authenticates user.

        Parameters
        ----------
        pwd_check : str
            Authentication string.

        Returns
        -------
        Union[bool, None]
            Returns if the user is correct.

        """

        serializer = Serializer(
            os.getenv('SECRET_KEY'),
            salt=self.password_hash)
        try:
            return serializer.loads(pwd_check.encode()) == self.id
        except (BadSignature, SignatureExpired, UnicodeError):
            #NOTE: I know we do not use signature expired,
            #NOTE: as we do not use timed token.
            #NOTE: Leaving this here for possible future changes.
            return None
