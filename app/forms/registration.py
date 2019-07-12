"""Registration Parser"""
from marshmallow import fields, validate
from flask_restplus import fields as frpf
from app.models.User import User as UserModel
from app.models.api import API
from .login import LoginSchema

REGISTER_DOC = API.model('Register', {
    'username': frpf.String(required=True),
    'password': frpf.String(required=True),
    'email': frpf.String(required=True),
})

class RegistrationSchema(LoginSchema):
    email = fields.String(
        required=True,
        validate=[
            validate.Length(**UserModel.EMAIL_LENGTH)
        ]
    )
