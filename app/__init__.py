"""Used to setup the app"""
from flask import Flask
from config import Config
from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from .extensions import mongo, login_manager, bcrypt, bootstrap5


def create_app():
    """App Factory Method"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    # Initialize plugins
    login_manager.init_app(app)
    mongo.init_app(app)
    bcrypt.init_app(app)
    bootstrap5.init_app(app)

    # register blueprints
    with app.app_context():
        app.register_blueprint(main_blueprint)
        app.register_blueprint(auth_blueprint)
        return app
