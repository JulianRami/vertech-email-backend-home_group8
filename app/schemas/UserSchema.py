from marshmallow import Schema, fields
from ..schemas.PlainSchema import PlainUserSchema, PlainEmailSchema

class UserSchema(PlainUserSchema):
    """
    Schema for representing user data.

    Attributes:
        received_emails (list): List of received emails.
        sent_emails (list): List of sent emails.
    """
    received_emails = fields.List(fields.Nested(PlainEmailSchema()), dump_only=True)
    sent_emails = fields.List(fields.Nested(PlainEmailSchema()), dump_only=True)

class UserLoginSchema(Schema):
    """
    Schema for validating user login data.

    Attributes:
        u_email (str): The email of the user.
        password (str): The password of the user.
    """
    u_email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)