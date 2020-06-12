import copy
import cerberus

from app.errors.custom_error import CustomError

types = {
    "email": {
        "type": "string",
        "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        "required": True
    },
    "password": {
        "type": "string",
        "required": True,
        "minlength": 6
    },
    "string": {
        "type": "string",
        "required": False,
        "nullable": True,
        "minlength": 0,
        "maxlength": 512
    },
    "integer": {
        "type": "integer",
        "required": False,
        "nullable": True
    },
}


def field(key: str, required=None, empty=None, nullable=None, allowed=None, minlength=None, maxlength=None, min=None, max=None):
    if key not in types:
        raise Exception("[{}] key not found in validator types".format(key))

    type = copy.deepcopy(types[key])

    if required is not None:
        type["required"] = required

    if empty is not None:
        type["empty"] = empty

    if nullable is not None:
        type["nullable"] = nullable

    if allowed is not None:
        type["allowed"] = allowed

    if minlength is not None:
        type["minlength"] = minlength

    if maxlength is not None:
        type["maxlength"] = maxlength

    if min is not None:
        type["min"] = min

    if max is not None:
        type["max"] = max

    return type


def validate(schema, body):
    v = cerberus.Validator(schema)

    if not v.validate(body):
        raise CustomError(message=v.errors, status_code=400)

    return body
