from app.database.db import db


class UserModel(db.Model):
    """
    Model class representing a user entity in the database.

    Attributes:
        id (int): The unique identifier for the user.
        name (str): The name of the user.
        u_email (str): The email address of the user.
        password (str): The hashed password of the user.
        sent_emails (relationship): Relationship attribute defining emails sent by the user.
        received_emails (relationship): Relationship attribute defining emails received by the user.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=False, nullable=False)
    u_email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    sent_emails = db.relationship("EmailModel", back_populates="sender", foreign_keys="[EmailModel.sender_id]",
                                  lazy="dynamic")
    received_emails = db.relationship("EmailModel", back_populates="recipient",
                                      foreign_keys="[EmailModel.recipient_id]", lazy="dynamic")

    @classmethod
    def find_by_u_email(cls, email):
        """
        Retrieve a user by their email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            UserModel or None: The user object if found, otherwise None.
        """
        return cls.query.filter_by(u_email=email).first()

    def json(self):
        """
        Serialize the UserModel object into a dictionary.

        Returns:
            dict: A dictionary representation of the UserModel object.
        """
        return {
            "name": self.name,
            "u_email": self.u_email,
        }

    def save_to_db(self):
        """
        Save the current UserModel object to the database.
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        Delete the current UserModel object from the database.
        """
        db.session.delete(self)
        db.session.commit()
