from flask import Blueprint, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from werkzeug.security import check_password_hash
from ..models import Users
from flask_login import login_user, LoginManager
from app import login_manager


# Blueprint Configuration
login_blueprint = Blueprint(
    "login_blueprint", __name__, template_folder="templates", static_folder="static"
)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Login page
@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check Hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successful")
                return redirect(url_for("dashboard"))
            else:
                flash("Wrong Password")
        else:
            flash("That user does not exist! Try again!")
    return render_template("login.html", form=form)


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
