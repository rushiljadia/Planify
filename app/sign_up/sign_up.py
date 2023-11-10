from flask import Blueprint, flash, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from ..models import Users
from .. import db

# Blueprint Configuration
sign_up_blueprint = Blueprint(
    "sign_up_blueprint", __name__, template_folder="templates", static_folder="static"
)


@sign_up_blueprint.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    name = None
    form = UserForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(
                name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                password_hash=form.password_hash.data,
            )
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.username.data = ""
        form.email.data = ""
        form.password_hash.data = ""
        flash("User Successfully Created!")
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
