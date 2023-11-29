from . import api
from ..main.forms import AddCourseForm
from flask import request


@api.route("/get-location/")
def get_location():
    form = AddCourseForm()
    location = request.form.get("")
