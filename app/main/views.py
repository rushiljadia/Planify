"""For handling the views of the apps main functionality"""
import json
from flask import render_template, request, flash, redirect
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
    """Handles the dashboard view of the app.
    In this view a user can add classes to their schedule and search for
    classes to add.
    A login is required to use this page

    Returns:
        render_template: Rendering of the dashboard page
    """
    form = AddCourseForm()
    # Connection to the mongoDB course collection
    course_collection = mongo.db.courses

    if request.method == "POST" and form.validate_on_submit:
        add_course(form, course_collection)

    return render_template("dashboard.html", form=form)


def get_course_info(form):
    # Getting the course name and formatting it to title case
    course_name = form.course_name.data.title()
    # Getting the course code and formmating it to all caps
    course_code = form.course_code.data.upper()
    # Getting the course number
    course_code_number = form.course_number.data
    # Creating the course prefix (i.e., ITCS 1212)
    course_prefix = f"{course_code} {course_code_number}"
    # Getting the address of where the course takes place
    course_place = form.place.data
    # Getting the days that the course takes place on as a list
    course_days = form.days.data
    # Getting the course start time
    course_start_time = form.start_time.data
    # Getting the course end time
    course_end_time = form.end_time.data
    # Getting if the course has a lab or not
    course_has_lab = form.has_lab.data
    # Getting the day that the lab takes place
    course_lab_day = form.lab_day.data
    # Getting the lab start time
    course_lab_start_time = form.lab_start_time.data
    # Getting the lab end time
    course_lab_end_time = form.lab_end_time.data

    if course_has_lab:
        course_to_add = {
            "name": course_name,
            "days": course_days,
            "start": str(course_start_time),
            "end": str(course_end_time),
            "code": course_prefix,
            "place": course_place,
            "lab": {
                "day": course_lab_day,
                "lab_start": str(course_lab_start_time),
                "lab_end": str(course_lab_end_time),
            },
        }
    else:
        course_to_add = {
            "name": course_name,
            "days": course_days,
            "start": str(course_start_time),
            "end": str(course_end_time),
            "code": course_prefix,
            "place": course_place,
            "lab": None,
        }

    return course_to_add


def add_course(form, course_collection):
    course_to_add = get_course_info(form)
    # Creating a query for an existing class to prevent duplicate
    # classes being added
    existing_class = course_collection.find_one(
        {
            "$or": [
                {"code": {"$regex": course_to_add["code"]}},
                {"name": {"$regex": course_to_add["name"]}},
            ]
        }
    )
    if existing_class is not None:
        flash("That course already exists!", category="danger")
    else:
        course_collection.insert_one(course_to_add)
        flash("Class added!", category="success")


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
