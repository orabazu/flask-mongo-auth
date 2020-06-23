import flask
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_cors import CORS
from dotenv import load_dotenv
# OR, explicitly providing path to '.env'
from pathlib import Path  # python3 only

import os

from app.api.user import userAPI
from app.errors.error_handlers import handle_custom_error
from app.errors.custom_error import CustomError
from app.api.middleware import Middleware

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
app = flask.Flask(__name__)
CORS(app, supports_credentials=True)
app.wsgi_app = Middleware(app.wsgi_app)
app.config["DEBUG"] = True
app.config["JWT_SECRET"] = os.getenv("JWT_SECRET"),
app.config["JWT_TTL"] = os.getenv("JWT_TTL"),
app.config['MONGODB_SETTINGS'] = {
    'db': os.getenv("DATABASE"),
    'host': os.getenv("HOST"),
    'alias': os.getenv("ALIAS")
}
app.register_error_handler(CustomError, handle_custom_error)

db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)

app.register_blueprint(userAPI)

if __name__ == '__main__':
    app.run()
