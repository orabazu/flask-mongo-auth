import bcrypt
import jwt
from time import time


def encrypt(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def check(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf8'), hashed_password)


def encode(payload, secret, ttl):
    payload['expires'] = int(time()) + (60 * int(ttl[0]))
    return jwt.encode(payload, secret[0], algorithm='HS256').decode("utf-8")


def decode(encoded, secret):
    return jwt.decode(encoded, secret, algorithms=['HS256'])
