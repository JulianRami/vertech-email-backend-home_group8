from marshmallow import Schema, fields
from ..schemas.UserSchema import PlainUserSchema, PlainEmailSchema

class EmailFormSchema(Schema):
    """
    Schema for validating email form data.

    Attributes:
        subject (str): The subject of the email.
        timestamp (datetime): The timestamp of the email.
        body (str): The body of the email.
        recipient_email (str): The email address of the recipient.
    """
    subject = fields.Str(required=True)
    timestamp = fields.DateTime()
    body = fields.Str(required=True)
    recipient_email = fields.Email(required=True)

class EmailSchema(PlainEmailSchema):
    """
    Schema for representing email data.

    Attributes:
        sender (PlainUserSchema): The sender of the email.
        recipient (PlainUserSchema): The recipient of the email.
    """
    sender = fields.Nested(PlainUserSchema(), dump_only=True)
    recipient = fields.Nested(PlainUserSchema(), dump_only=True)
