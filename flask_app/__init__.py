# 3rd-party packages
from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from .google.routes import setup_google_oauth


# stdlib
from datetime import datetime
import os

# local
from .client import MovieClient


db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()

from .users.routes import users
from .movies.routes import movies
from .google.routes import google


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    setup_google_oauth(app)

    app.register_blueprint(google)
    app.register_blueprint(users)
    app.register_blueprint(movies)

    login_manager.login_view = "users.login"

    return app
