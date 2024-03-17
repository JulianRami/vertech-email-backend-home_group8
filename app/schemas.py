from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    """
    Schema for representing plain user data.

    Attributes:
        name (str): The name of the user.
        u_email (str): The email of the user.
        password (str): The password of the user.
    """
    #id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    u_email = fields.Email(required=True)
    # Never return password
    password = fields.Str(required=True, load_only=True)


class PlainEmailSchema(Schema):
    """
    Schema for representing plain email data.

    Attributes:
        id (int): The ID of the email.
        subject (str): The subject of the email.
        body (str): The body of the email.
        timestamp (datetime): The timestamp of the email.
    """
    id = fields.Int(dump_only=True)
    subject = fields.Str(required=True)
    body = fields.Str(required=True)
    timestamp = fields.DateTime()


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

class UserLoginSchema(Schema):
    """
    Schema for validating user login data.

    Attributes:
        u_email (str): The email of the user.
        password (str): The password of the user.
    """
    u_email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class EmailSchema(PlainEmailSchema):
    """
    Schema for representing email data.

    Attributes:
        sender (PlainUserSchema): The sender of the email.
        recipient (PlainUserSchema): The recipient of the email.
    """
    sender = fields.Nested(PlainUserSchema(), dump_only=True)
    recipient = fields.Nested(PlainUserSchema(), dump_only=True)


class UserSchema(PlainUserSchema):
    """
    Schema for representing user data.

    Attributes:
        received_emails (list): List of received emails.
        sent_emails (list): List of sent emails.
    """
    received_emails = fields.List(fields.Nested(PlainEmailSchema()), dump_only=True)
    sent_emails = fields.List(fields.Nested(PlainEmailSchema()), dump_only=True)


