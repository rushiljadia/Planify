from . import main
from .forms import add_course_form
from flask import render_template
from flask_login import login_required


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = add_course_form()
    return render_template("dashboard.html", form=form)
