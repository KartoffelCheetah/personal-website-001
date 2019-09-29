"""A form to handle the registration"""
from marshmallow import fields, validate, post_load
from flask_restplus import fields as frpf
from app.models.user_entity import UserEntity
from app.models.api import API
from .login import LoginSchema

REGISTER_DOC = API.model('Register', {
    'username': frpf.String(required=True),
    'password': frpf.String(required=True),
    'email': frpf.String(required=True),
})

class RegistrationSchema(LoginSchema):
    """Validation"""
    email = fields.Email(
        required=True,
        validate=[
            validate.Length(**UserEntity.EMAIL_LENGTH)
        ]
    )

    @post_load
    def create_user(self, data, **kwargs): #pylint: disable=R0201, W0613
        """After validation passes creates a user."""
        return UserEntity(
            username=data['username'],
            email=data['email'],
            password_hash=UserEntity.get_hashed_password(data['password']),
        )
