"""Forms for the user login and registration pages
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    """User login form"""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegistrationForm(FlaskForm):
    """User registration form"""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=24)]
    )
    password = PasswordField(
        "Password", validators=[Length(min=8, message="Password to short!")]
    )
    confirm = PasswordField(
        "Confirm Password",
        validators=[EqualTo("password", message="Password Mismatch")],
    )
    submit = SubmitField("Submit")
