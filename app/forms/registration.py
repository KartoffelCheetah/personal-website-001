"""Registration Parser"""
from app.validators import length
from app.models.User import User as UserModel
from .base import BASE_PARSER

REGISTRATION_PARSER = BASE_PARSER.copy()

REGISTRATION_PARSER.add_argument(
    'username',
    type=length(UserModel.USERNAME_LENGTH[0], UserModel.USERNAME_LENGTH[1], str),
    required=True,
    location='form',
).add_argument(
    'password',
    type=length(UserModel.PASSWORD_LENGTH[0], UserModel.PASSWORD_LENGTH[1], str),
    required=True,
    location='form',
).add_argument(
    'email',
    type=length(UserModel.EMAIL_LENGTH[0], UserModel.EMAIL_LENGTH[1], str),
    required=True,
    location='form',
)
