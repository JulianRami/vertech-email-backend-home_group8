from app.database.db import db


class EmailModel(db.Model):
    """
    Model class representing an email entity in the database.

    Attributes:
        id (int): The unique identifier for the email.
        subject (str): The subject of the email.
        body (str): The body content of the email.
        timestamp (datetime): The timestamp when the email was created.
        sender_id (int): The foreign key referencing the sender's user ID.
        recipient_id (int): The foreign key referencing the recipient's user ID.
        sender (relationship): Relationship attribute defining the sender of the email.
        recipient (relationship): Relationship attribute defining the recipient of the email.
    """
    __tablename__ = "emails"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    sender = db.relationship("UserModel", foreign_keys=[sender_id], back_populates="sent_emails")
    recipient = db.relationship("UserModel", foreign_keys=[recipient_id], back_populates="received_emails")

    def json(self):
        """
        Serialize the EmailModel object into a dictionary.

        Returns:
            dict: A dictionary representation of the EmailModel object.
        """
        return {
            "id": self.id,
            "body": self.body,
            "sender": self.sender,
            "recipient": self.recipient
        }

    @classmethod
    def find_all_sent_by_user(cls, id):
        """
        Retrieve all emails sent by a user with the given ID.

        Args:
            id (int): The ID of the user.

        Returns:
            list: A list of EmailModel objects representing emails sent by the user.
        """
        return cls.query.filter_by(sender_id=id).all()

    @classmethod
    def find_all_received_by_user(cls, id):
        """
        Retrieve all emails received by a user with the given ID.

        Args:
            id (int): The ID of the user.

        Returns:
            list: A list of EmailModel objects representing emails received by the user.
        """
        return cls.query.filter_by(recipient_id=id).all()

    def save_to_db(self):
        """
        Save the current EmailModel object to the database.
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        Delete the current EmailModel object from the database.
        """
        db.session.delete(self)
        db.session.commit()
