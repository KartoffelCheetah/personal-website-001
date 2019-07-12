"""User Model"""

import os
import datetime
from typing import Union, Dict
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
from app.models.db import DB
from .Base import Base as BaseModel

load_dotenv(dotenv_path=find_dotenv('.env'))

class User(BaseModel, UserMixin, DB.Model):
    """user table"""

    USERNAME_LENGTH: Dict[str, int] = {'min': 6, 'max': 64}
    EMAIL_LENGTH: Dict[str, int] = {'min': 5, 'max': 128}
    PASSWORD_LENGTH: Dict[str, int] = {'min': 8, 'max': 256}
    # Block user when reaches this limit
    LOGIN_COUNT_LIMIT: int = 10
    # Timer to reset LOGIN_COUNT_LIMIT to 0
    LOGIN_COUNT_RESET: int = 600
    #pylint: disable=E1101
    username = DB.Column(DB.String(USERNAME_LENGTH['max']), unique=True, nullable=False)
    email = DB.Column(DB.String(EMAIL_LENGTH['max']), unique=True, nullable=False)
    password_hash = DB.Column(DB.String(256), nullable=False)
    login_count = DB.Column(DB.Integer, nullable=False, default=0)
    last_try = DB.Column(DB.DateTime(), nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return '<User %r>' % self.username

    def is_password_correct(self, password: str) -> bool:
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
    def get_hashed_password(password: str) -> str:
        """Gets hashed password from plain text password.

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
            #NOTE: SignatureExpired could happen only when using
            #NOTE: TimedJSONWebSignatureSerializer.
            return None
