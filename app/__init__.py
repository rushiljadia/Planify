from flask import Flask
from config import Config

from .extensions import mongo, login_manager, bcrypt


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    # Initialize plugins
    login_manager.init_app(app)
    mongo.init_app(app)
    bcrypt.init_app(app)

    # register blueprints
    with app.app_context():
        # from .login import login
        # from .sign_up import sign_up

        # app.register_blueprint(login.login_blueprint)
        # app.register_blueprint(sign_up.sign_up_blueprint)

        from .main import main as main_blueprint
        from .auth import auth as auth_blueprint

        app.register_blueprint(main_blueprint)
        app.register_blueprint(auth_blueprint)
        return app
