from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from ..models.user import UserModel
from ..schemas.UserSchema import UserSchema, UserLoginSchema
from ..schemas.PlainSchema import PlainUserSchema

from sqlalchemy.exc import IntegrityError

blp = Blueprint("users", __name__, description="Operations on users.")


@blp.route("/api/register")
class UserRegister(MethodView):
    """
    Method view for registering a new user.

    Attributes:
        post: Handles POST requests for user registration.
    """
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """
        Handle POST request to register a new user.

        Args:
            user_data (dict): The data for user registration.

        Returns:
            tuple: A tuple containing a success message and HTTP status code 201.
        """
        user = UserModel(
            name=user_data["name"],
            u_email=user_data["u_email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        try:
            user.save_to_db()

            return {"message": "User created successfully."}, 201
        except IntegrityError:
            abort(
                400,
                message="Username already exists."
            )


@blp.route("/api/login")
class UserLogin(MethodView):
    """
    Method view for user login.

    Attributes:
        post: Handles POST requests for user login.
    """
    @blp.arguments(UserLoginSchema)
    def post(self, user_data):
        """
        Handle POST request for user login.

        Args:
            user_data (dict): The data for user login.

        Returns:
            tuple: A tuple containing an access token and user details if login is successful, 
                   otherwise raises HTTP status code 401.
        """
        user = UserModel.find_by_u_email(user_data["u_email"])

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True, expires_delta=timedelta(weeks=1))
            return {"access_token": access_token, **user.json()}, 200

        abort(401, message="Invalid credentials.")


@blp.route("/api/users")
class Users(MethodView):
    """
    Method view for retrieving users.

    Attributes:
        get: Handles GET requests for retrieving users.
    """
    @jwt_required()
    @blp.response(200, PlainUserSchema(many=True))
    def get(self):
        """
        Handle GET request to retrieve all users.

        Returns:
            list: A list of user details.
        """
        users = UserModel.query.all()
        return users
