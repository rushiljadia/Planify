from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from werkzeug.security import check_password_hash
from flask_login import login_user, LoginManager, current_user, logout_user
from app import login_manager
from ..extensions import mongo, login_manager
from bcrypt import hashpw

login_manager.login_view = "login"

# Blueprint Configuration
login_blueprint = Blueprint(
    "login_blueprint", __name__, template_folder="templates", static_folder="static"
)


class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    """
    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)
    """

    @staticmethod
    def check_password(password, password_hash):
        return hashpw(password, password_hash)


@login_manager.user_loader
def load_user(username):
    u = mongo.db.users.find_one({"name": username})
    if not u:
        return None

    return User(username=u["name"])


# Login page
@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({"name": form.username.data})

        if user and User.check_password(
            form.password.data.encode("utf-8"), user["password"]
        ):
            user_obj = User(username=user["name"])
            login_user(user_obj)
            return redirect("/dashboard")

        else:
            flash("Invalid username or password")
    return render_template("login.html", title="Sign In", form=form)


@login_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
