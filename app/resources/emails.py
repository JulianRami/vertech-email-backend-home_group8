from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..schemas.EmailSchema import EmailFormSchema,EmailSchema
from ..models.email import EmailModel
from sqlalchemy.exc import SQLAlchemyError
from ..models.user import UserModel


blp = Blueprint("emails", __name__, description="Operation on emails")


@blp.route("/api/emails")
class Email(MethodView):
    """
    Method view for handling email operations.

    Attributes:
        post: Handles POST requests for creating a new email.
    """
    @jwt_required()
    @blp.arguments(EmailFormSchema)
    @blp.response(201, EmailFormSchema)
    def post(self, email_data):
        """
        Handle POST request to create a new email.

        Args:
            email_data (dict): The data for creating the email.

        Returns:
            tuple: A tuple containing the created email and HTTP status code 201.
        """
        current_user_id = get_jwt_identity()
        recipient = UserModel.query.filter(
            UserModel.u_email == email_data["recipient_email"]
        ).first()

        if recipient is None:
            abort(404, message="Recipient not found")

        email_data.pop("recipient_email")
        email = EmailModel(sender_id=current_user_id,
                           recipient_id=recipient.id, **email_data)

        try:
            email.save_to_db()
            return email, 201
        except SQLAlchemyError as e:
            abort(500, message="An error occurred while inserting the email.")

@blp.route("/api/emails")
class Emails(MethodView):
    """
    Method view for handling email retrieval.

    Attributes:
        get: Handles GET requests for received emails.
    """
    @jwt_required()
    @blp.response(200, EmailSchema(many=True))
    def get(self):
        """
        Handle GET request to received emails.

        Returns:
            list: A list of received emails.
        """
        current_user_id = get_jwt_identity()
        try:
            received_emails = EmailModel.query.filter_by(recipient_id=current_user_id, received_deleted=False).all()
            return received_emails
        except SQLAlchemyError as e:
            abort(500, message="Failed to fetch emails.")


@blp.route("/api/emails/<int:email_id>")
class EmailDetail(MethodView):
    """
    Method view for handling email details retrieval.

    Attributes:
        get: Handles GET requests for retrieving details of a specific received email.
    """
    @jwt_required()
    @blp.response(200, EmailSchema())
    def get(self, email_id):
        """
        Handle GET request to retrieve details of a specific received email.

        Args:
            email_id (int): The ID of the email to retrieve.

        Returns:
            EmailModel: The details of the requested email.
        """
        current_user_id = get_jwt_identity()
        try:
            email = EmailModel.query.filter_by(id=email_id, recipient_id=current_user_id, received_deleted=False).first()
            if email is None:
                abort(404, message="Email not found or unauthorized.")
            return email
        except SQLAlchemyError as e:
            abort(500, message="Failed to fetch email details.")


@blp.route("/api/emails/sent")
class EmailsSent(MethodView):
    """
    Method view for handling sent email retrieval.

    Attributes:
        get: Handles GET requests for retrieving sent emails.
    """
    @jwt_required()
    @blp.response(200, EmailSchema(many=True))
    def get(self):
        """
        Handle GET request to retrieve sent emails.

        Returns:
            list: A list of sent emails.
        """
        current_user_id = get_jwt_identity()
        try:
            sent_emails = EmailModel.query.filter_by(sender_id=current_user_id, sent_deleted=False).all()
            return sent_emails
        except SQLAlchemyError as e:
            abort(500, message="Failed to fetch sent emails.")


@blp.route("/api/emails/<int:email_id>")
class EmailReceivedDelete(MethodView):
    """
    Method view for handling received email deletion.

    Attributes:
        delete: Marks as deleted requests a specific received email.
    """
    @jwt_required()
    @blp.response(204)
    def patch(self, email_id):
        """
        Handle PATCH request to mark as deleted a specific received email.

        Args:
            email_id (int): The ID of the email to patch email as deleted.

        Returns:
            tuple: A tuple containing an empty response and HTTP status code 204.
        """
        current_user_id = get_jwt_identity()
        try:
            email = EmailModel.query.filter_by(id=email_id, recipient_id=current_user_id).first()
            if email is None:
                abort(404, message="Email not found or unauthorized.")
            email.mark_as_deleted("received")
            return {}, 204
        except SQLAlchemyError as e:
            abort(500, message="Failed to delete email.")


@blp.route("/api/emails/sent/<int:email_id>")
class EmailSentDelete(MethodView):
    """
    Method view for handling sent email deletion.

    Attributes:
        delete: Marks as deleted requests for deleting a specific sent email.
    """
    @jwt_required()
    @blp.response(204)
    def patch(self, email_id):
        """
        Handle PATCH request to mark as deleted a specific sent email.

        Args:
            email_id (int): The ID of the email to patch email as deleted.

        Returns:
            tuple: A tuple containing an empty response and HTTP status code 204.
        """
        current_user_id = get_jwt_identity()
        try:
            email = EmailModel.query.filter_by(id=email_id, sender_id=current_user_id).first()
            if email is None:
                abort(404, message="Email not found or unauthorized.")
            email.mark_as_deleted("sent")
            return {}, 204
        except SQLAlchemyError as e:
            abort(500, message="Failed to delete email.")