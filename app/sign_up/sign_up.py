from flask import Blueprint, flash, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from ..models import User

# Blueprint Configuration
sign_up_blueprint = Blueprint(
    "sign_up_blueprint", __name__, template_folder="templates", static_folder="static"
)


@sign_up_blueprint.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    name = None
    form = UserForm()
    return render_template("sign_up.html", name=name, form=form)


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField(
        "Password", validators=[Length(min=8, message="Password to short!")]
    )
    confirm = PasswordField(
        "Confirm Password", validators=[EqualTo("password_hash", "Password Mismatch")]
    )
    submit = SubmitField("Submit")
