from . import api
from ..main.forms import add_course_form
from flask import request

@api.route("/get-location/")
def get_location():
    form = add_course_form()
    location = request.form.get("")