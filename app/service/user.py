from flask import current_app

from app.utils.password import encrypt, encode, check
from app.errors.custom_error import CustomError
from app.model.user import User


def register(user):
    try:
        active_user = User.objects(email=user.email).first()
        if not active_user:
            user.password = encrypt(user.password)
            user.save()
        else:
            raise CustomError()
    except:
        raise CustomError(
            message="Email or username has already been used.",
            status_code=400,
        )

    current_app.logger.debug("User with email %s registered" % user.email)

    return encode(user.jwt_payload(), current_app.config["JWT_SECRET"], current_app.config["JWT_TTL"])


def login(email, password, last_login_ip):
    active_user = User.objects(email=email).first()

    if not active_user or not check(password, active_user.password):
        raise CustomError(
            message="Wrong mail or password.",
            status_code=401,
        )

    active_user.update(set__last_login_ip=last_login_ip)
    current_app.logger.debug("User with email %s logged in" % active_user.email)

    return encode(active_user.jwt_payload(), current_app.config["JWT_SECRET"], current_app.config["JWT_TTL"])
