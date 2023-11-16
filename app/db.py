from flask import request
from extensions import mongo

db = mongo.planify
users = db.users
courses = db.courses


def add_course():
    if request.method == "POST":
        name = request.form.get("name")
        place = request.form.get("place")
        start_time = request.form.get("start")
        end_time = request.form.get("end")
