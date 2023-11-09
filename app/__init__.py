from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    # TODO: THIS SHOULD BE HIDDEN IN PRODUCTION
    app.config["SECRET_KEY"] = "key"

    # Initialize DB

    # Add MySQL Database
    # TODO: HIDE IN PRODUCTION
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "mysql+pymysql://root:nevereatsoggywafflesclock@localhost/planify"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import Users

    return app
