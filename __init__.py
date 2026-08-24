from flask import Flask
from .config import settings
from .db import close_driver
from .routes import bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = settings.flask_secret_key
    app.register_blueprint(bp)
    app.teardown_appcontext(lambda exc=None: None)
    return app
