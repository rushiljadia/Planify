"""For handling the views of the apps main functionality"""
from flask import render_template, request, flash, jsonify, session
from flask_login import login_required, current_user
from bson import ObjectId, json_util
import re
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
    if request.method == "POST" and form.validate_on_submit():
        add_course(form, course_collection)

    return render_template("dashboard.html", form=form)


def get_course_info(form):
    """Gets the course information from the course adding form

    Args:
        form (Form): The class adding form to pull from

    Returns:
        dict: A dictionary structured to add to the databse
    """
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


@main.route("/add-class", methods=["POST"])
def add_class():
    try:
        course_info = request.get_json().get("courseInfo")

        if course_info:
            course_id = mongo.db.courses.find_one({"name": course_info["name"]})["_id"]

            # Convert specified days to a list to ensure consistency
            specified_days = course_info.get("days", [])
            if not isinstance(specified_days, list):
                specified_days = list(specified_days)

            # Filter out unwanted characters from specified days
            specified_days = [
                day for day in specified_days if day in ["M", "T", "W", "R", "F"]
            ]

            # Check for conflicts on all days in the user's schedule
            user_schedule = mongo.db.users.find_one(
                {"name": current_user.username}, {"schedule": 1}
            )["schedule"]

            for day, courses in user_schedule.items():
                if day in specified_days:
                    # Check for conflicts with courses on the same day
                    if course_id in courses:
                        return (
                            jsonify(
                                {"message": f"Conflict: Course already exists on {day}"}
                            ),
                            400,
                        )
                else:
                    # Check for conflicts with courses on different days
                    if course_id in courses:
                        return (
                            jsonify(
                                {
                                    "message": f"Conflict: Course already exists on a conflicting day ({day})"
                                }
                            ),
                            400,
                        )

            # No conflicts detected, proceed to add the class for each day
            for day in specified_days:
                result = mongo.db.users.update_one(
                    {
                        "name": current_user.username,
                        f"schedule.{day}": {"$nin": [course_id]},
                    },
                    {"$push": {f"schedule.{day}": {"$each": [course_id]}}},
                )

                if result.modified_count == 0:
                    # Failed to add class for this day
                    return jsonify({"message": f"Error adding class for {day}"}), 400

            return jsonify({"message": "Class added successfully"})

        else:
            return jsonify({"message": "Error: Missing courseInfo"}), 400

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


@main.route("/get-schedule", methods=["GET"])
def get_schedule():
    user_schedule = current_user.schedule

    # Create a list to store the modified schedule data
    modified_schedule = []

    # Iterate over each day in the schedule
    for day, class_ids in user_schedule.items():
        # Fetch course information for each class ID
        class_info_list = []
        for class_id in class_ids:
            # Convert ObjectId to string
            class_id_str = str(class_id)

            # Fetch course information from the 'courses' collection
            course_data = get_course_data(class_id_str)

            # Add course information to the list
            class_info_list.append(course_data)

        # Append day and class information to the modified schedule
        modified_schedule.append({"day": day, "classes": class_info_list})

    # Use json_util.dumps to handle serialization of ObjectId
    json_data = json_util.dumps(modified_schedule)

    # Return the JSON response
    return json_data, 200, {"Content-Type": "application/json"}


@main.route("/get-course/<course_id>", methods=["GET"])
def get_course_data(course_id):
    # Fetch course information from the 'courses' collection
    # You need to replace 'courses' with the actual name of your collection
    course_data = mongo.db.courses.find_one({"_id": ObjectId(course_id)})
    print(course_data["name"])

    # Return relevant course information
    if course_data:
        return {
            "_id": str(course_data["_id"]),
            "courseName": course_data["name"],
            "coursePlace": course_data["place"],
            "startTime": course_data["start"],
            "endTime": course_data["end"],
            "courseCode": course_data["code"],
        }
    else:
        return {}
