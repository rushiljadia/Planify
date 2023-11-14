from flask import Flask
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from .extensions import db

# Globally accessable libraries
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    # Initialize plugins
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # register blueprints
    with app.app_context():
        from .home import home
        from .login import login
        from .dashboard import dashboard
        from .sign_up import sign_up

        app.register_blueprint(home.home_blueprint)
        app.register_blueprint(login.login_blueprint)
        app.register_blueprint(dashboard.dashboard_blueprint)
        app.register_blueprint(sign_up.sign_up_blueprint)
        return app
