from marshmallow import Schema, fields, validate
from src.libs import constants


class RegistrationSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(
        min=3, max=constants.USERNAME_LENGTH))
    email = fields.Email(required=True)
    password = fields.Str(
        required=True, validate=validate.Length(min=6, max=8))


class LoginSchema(Schema):
    remember = fields.Str()
    email = fields.Email(required=True)
    password = fields.Str(
        required=True, validate=validate.Length(min=6, max=8))
