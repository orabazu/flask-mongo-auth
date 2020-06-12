from flask import Blueprint, request, jsonify, g
from app.config import URL_PREFIX
from app.api.validator import field, validate
from app.model.user import User
from app.service.user import register as service_register, login as service_login


url_prefix = f"{URL_PREFIX}/user"
userAPI = Blueprint("user", __name__,  url_prefix=url_prefix)


@userAPI.route("/", methods=['GET'])
def get():
    """Simple health check service"""
    users = User.objects
    return jsonify({"status": users})


@userAPI.route("/health-check", methods=['GET'])
def health_check():
    """Simple health check service"""
    return jsonify({"status": "sdas"})


@userAPI.route("/register", methods=['POST'])
def register():
    """Register user"""
    body = validate({
        "email": field("email"),
        "password": field("password"),
    }, request.get_json(force=True, silent=True))

    user = User(**body)
    user.registration_ip = request.remote_addr
    user.last_login_ip = request.remote_addr

    token = service_register(user)

    return jsonify({"status": "OK", "token": token})


@userAPI.route("/login", methods=['POST'])
def login():
    """Login user"""
    body = validate({
        "email": field("email"),
        "password": field("password")
    }, request.get_json(force=True, silent=True))

    token = service_login(
        body["email"],
        body["password"],
        request.remote_addr
    )

    return jsonify({"status": "OK", "token": token})
