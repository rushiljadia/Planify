from flask import render_template, request
from flask_login import login_required
from . import main
from .forms import AddCourseForm
from ..extensions import mongo


@main.route("/")
def index():
    """Route for the homepage of the website"""
    return render_template("index.html")


@main.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = AddCourseForm()

    if request.method == "POST":
        course_collection = mongo.db.courses
        course_name = request.form.get("course_name").title()
        course_code = request.form.get("course_code").upper()
        course_code_number = request.form.get("course_number")

        course_prefix = f"{course_code} {course_code_number}"

        course_place = request.form.get("course_place")
        course_days = request.form.get("course_days")
        course_start_time = request.form.get("start_time")
        course_end_time = request.form.get("end_time")
        course_has_lab = request.form.get("has_lab")
        course_lab_day = request.form.get("lab_day")
        course_lab_start_time = request.form.get("lab_start_time")
        course_lab_end_time = request.form.get("lab_end_time")

        existing_class = course_collection.find_one(
            {
                "$or": [
                    {"code": {"$regex": course_prefix}},
                    {"name": {"$regex": course_name}},
                ]
            }
        )

        print(course_name)
        print(course_prefix)
        print(course_place)
        print(course_days)
        print(course_start_time)
        print(course_end_time)
        print(course_has_lab)
        print(course_lab_day)
        print(course_lab_start_time)
        print(course_lab_end_time)

    return render_template("dashboard.html", form=form)


@main.route("/search", methods=["GET", "POST"])
def search():
    """Used by the user to search for classes that exist in the database"""
    # Connection to the courses collection of the database
    courses = mongo.db.courses

    # Getting the users input from the search bar
    q = request.args.get("q")

    # Users can serach by course code or course name
    if q:
        results = list(
            courses.find(
                {
                    "$or": [
                        {"code": {"$regex": q.upper()}},
                        {"name": {"$regex": q.title()}},
                    ]
                }
            )
        )
    else:
        # If no results are found, an empty list is given
        results = []

    return render_template("search_results.html", results=results)
