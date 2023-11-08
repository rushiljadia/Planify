from flask import Blueprint, render_template, request, flash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@auth.route("/logout")
def logout():
    return "<p>Logout</p>"


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        password = request.form.get("password-1")
        password_two = request.form.get("password-2")

        if len(email) < 4:
            flash("Email must be more than 3 characters!", category="error")
        elif len(first_name) < 2:
            flash("First name must be more than 1 character!", category="error")
        elif password != password_two:
            flash("Passwords do not match!", category="error")
        elif len(password) < 7:
            flash("Password must be at least 7 characters", category="error")
        else:
            # add to database
            flash("Account created successfully!", category="success")

    return render_template("sign_up.html")
