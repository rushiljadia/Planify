from . import auth
from .forms import LoginForm, RegistrationForm
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, current_user, logout_user, login_required
from ..extensions import mongo
from ..db import User
from bcrypt import hashpw, gensalt


# Login page
@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({"name": form.username.data})

        if user and User.check_password(form.password.data.encode(), user["password"]):
            user_obj = User(username=user["name"])
            login_user(user_obj)
            return redirect("/dashboard")

        else:
            flash("Invalid username or password")
    return render_template("auth/login.html", title="Sign In", form=form)


# Logout function
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    name = None
    form = RegistrationForm()
    if request.method == "POST":
        user_collection = mongo.db.users
        username = request.form.get("username").lower()
        existing_user = user_collection.find_one({"name": username})

        # if the user does not exist in the database a new account is made for them
        if existing_user is None:
            # Hashing user password
            password_hash = hashpw(
                request.form.get("password").encode("utf-8"), gensalt()
            )
            user_collection.insert_one(
                {
                    "name": username,
                    "password": password_hash,
                    "schedules": [],
                }
            )
            session["username"] = username
            return redirect(url_for("main.dashboard"))

        # if the username is already in use the user should choose a new name or login
        flash(
            "That username is already in use! Please try a different username or login"
        )

    # if the method is GET the page is returned
    return render_template("auth/sign_up.html", name=name, form=form)
