from flask import Blueprint, render_template, request
from wtforms import Form, StringField
from os import path
import json

# Blueprint Configuration
dashboard_blueprint = Blueprint(
    "dashboard_blueprint", __name__, template_folder="templates", static_folder="static"
)


@dashboard_blueprint.route("/dashboard", methods=["GET", "POST"])
# @login_required
def dashboard():
    SITE_ROOT = path.realpath(path.dirname(__file__))
    json_url = path.join(SITE_ROOT, "static/data", "places.json")
    data = json.load(open(json_url))
    return render_template("dashboard.html", places=data)
