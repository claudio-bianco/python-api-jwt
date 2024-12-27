from marshmallow import Schema, fields, validate
from flask import Flask, request, make_response
from flask_cors import CORS
import jwt
from datetime import datetime as dt
from functools import wraps
import datetime

app = Flask(__name__)
CORS(app)

SECRET_KEY = "chanduthedev"
static_users = {
    "test": {"user_name": "test", "password": "test"},
    "admin": {"user_name": "admin", "password": "admin"},
}


def make_error_response(err_msg, status_code):
    return {
        "message": err_msg,
    }, status_code


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        # reading token from header
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return make_error_response("Authentication Token is missing!", 400)
        try:
            # decoding jwt token with secret
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            # verifying whether token is belogns to current user
            current_user = static_users.get(data["user_name"])
            if current_user is None:
                return make_error_response("Invalid Authentication token!", 401)

            # Convert the expiration time to a datetime object
            expiration_datetime = dt.utcfromtimestamp(data["exp"])
            # Get the current time
            current_time = dt.utcnow()

            # Check if the token has expired
            if current_time > expiration_datetime:
                return make_error_response("Token has expired", 401)
            # token is valid, process the request
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return make_error_response("Token has expired", 401)
        except jwt.InvalidTokenError:
            return make_error_response("Token is invalid", 401)

    return decorated


class LoginInputSchema(Schema):
    user_name = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=4))


def login_user(input_data):
    create_validation_schema = LoginInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return make_error_response(errors, 400)

    user_details = static_users.get(input_data.get("user_name"), None)
    if user_details is None:
        return make_error_response("User or password not valid.", 400)

    # checkin password
    password = user_details.get("password", None)
    if input_data.get("password") == password:
        # jwt paylaod
        payload = {
            "user_name": input_data.get("user_name"),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
        }
        # creating JWT token with expiry of 5mins
        token = jwt.encode(payload, SECRET_KEY)

        # Appending token in the login success response
        return {
            "data": {"user_name": input_data.get("user_name"), "token": token},
            "message": "User login successfully",
        }, 200

    else:
        return make_error_response("Invalid username or password", 400)


@app.route("/login", methods=["POST"])
def login():
    input_data = request.get_json()
    response, status = login_user(input_data)
    return make_response(response, status)


@app.route("/products", methods=["GET"])
@token_required
def get_products():
    return {
        "data": {"products": ["product1", "product2"]},
        "message": "success",
    }, 200


if __name__ == "__main__":
    app.run(port=5007, debug=True)