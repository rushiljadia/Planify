from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, redirect, url_for, flash, request, session
from bcrypt import hashpw, gensalt
from . import auth
from .forms import LoginForm, RegistrationForm
from ..extensions import mongo
from ..db import User


# Login page
@auth.route("/login", methods=["GET", "POST"])
def login():
    """Function that logs a user in

    Returns:
        template: the login page
    """
    # If a logged in user tries to log in they are
    # redirected back to the home page
    if current_user.is_authenticated:
        return redirect("/")

    # Form that the page uses to log a user in
    form = LoginForm()
    if form.validate_on_submit():
        # Attempting to find a username that matches what the user has entered
        user = mongo.db.users.find_one({"name": form.username.data})

        # Checking the user name and the password that the user entered
        # matches to one in the database
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
    """Method used to logout

    Returns:
        redirect: redirects the user to the login page
    """
    logout_user()
    return redirect("/login")


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    """Route to the user sign up page"""
    name = None
    # Form used by the page to sign up
    form = RegistrationForm()
    if request.method == "POST":
        # Database user collection connection
        user_collection = mongo.db.users
        # Getting the user name from the form input
        username = request.form.get("username").lower()
        # Attempting to find the user based on their user name
        existing_user = user_collection.find_one({"name": username})

        # Ff the user does not exist a new account is made for them
        if existing_user is None:
            # Hashing user password
            password_hash = hashpw(
                request.form.get("password").encode("utf-8"), gensalt()
            )
            # Inserting the user into the collection
            user_collection.insert_one(
                {
                    "name": username,
                    "password": password_hash,
                    "schedules": [],
                }
            )
            # Updating the session for the now logged in user
            session["username"] = username
            # Redirect the user back to their dashboard
            return redirect(url_for("main.dashboard"))

        # if the username is already in use the user should choose a
        # new name or login
        flash("That username is already taken! Try a different username or login")

    # if the method is GET the page is returned
    return render_template("auth/sign_up.html", name=name, form=form)
