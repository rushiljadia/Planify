from . import main
from .forms import add_course_form
from ..extensions import mongo
from ..api.geocoding import get_location
from flask import render_template, request, redirect
from flask_login import login_required


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = add_course_form()
    return render_template("dashboard.html", form=form)


@main.route("/search", methods=["GET", "POST"])
def search():
    courses = mongo.db.courses

    q = request.args.get("q")
    print(q)

    if q:
        results = list(courses.find({"code": {"$regex": q}}))
    else:
        results = []

    return render_template("search_results.html", results=results)
