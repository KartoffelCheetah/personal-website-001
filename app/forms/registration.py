"""Registration Parser"""
from app.validators import length
from app.models.User import User as UserModel
from .login import LOGIN_PARSER

REGISTRATION_PARSER = LOGIN_PARSER.copy()

REGISTRATION_PARSER.add_argument(
    'email',
    type=length(UserModel.EMAIL_LENGTH[0], UserModel.EMAIL_LENGTH[1], str),
    required=True,
    location='form',
)
