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