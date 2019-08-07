"""Login Parser"""
from marshmallow import Schema, fields, validate
from flask_restplus import fields as frpf
from app.models.api import API
from app.models.user_entity import UserEntity

LOGIN_DOC = API.model('Login', {
    'username': frpf.String(required=True),
    'password': frpf.String(required=True),
})

class LoginSchema(Schema):
    username = fields.String(
        required=True,
        validate=[
            validate.Length(**UserEntity.USERNAME_LENGTH)
        ]
    )
    password = fields.String(
        required=True,
        validate=[
            validate.Length(**UserEntity.PASSWORD_LENGTH)
        ]
    )
