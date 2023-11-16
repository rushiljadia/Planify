from flask import Blueprint, flash, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug.security import generate_password_hash
from ..extensions import mongo
from bcrypt import hashpw, gensalt

# Blueprint Configuration
sign_up_blueprint = Blueprint(
    "sign_up_blueprint", __name__, template_folder="templates", static_folder="static"
)


@sign_up_blueprint.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    name = None
    form = UserForm()
    if request.method == "POST":
        user_collection = mongo.db.users
        existing_user = user_collection.find_one({"name": request.form.get("username")})

        # if the user does not exist in the database a new account is made for them
        if existing_user is None:
            # Hashing user password
            password_hash = hashpw(
                request.form.get("password").encode("utf-8"), gensalt()
            )
            user_collection.insert_one(
                {"name": request.form.get("username"), "password": password_hash}
            )
            session["username"] = request.form.get("username")
            return redirect(url_for("home"))

        # if the username is already in use the user should choose a new name or login
        return (
            "That username is already in use! Please try a different username or login"
        )

    # if the method is GET the page is returned
    return render_template("sign_up.html", name=name, form=form)


class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Password", validators=[Length(min=8, message="Password to short!")]
    )
    confirm = PasswordField(
        "Confirm Password", validators=[EqualTo("password", "Password Mismatch")]
    )
    submit = SubmitField("Submit")
