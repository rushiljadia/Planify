from flask import Blueprint, render_template, request
from wtforms import Form, StringField
from os import path


# Blueprint Configuration
dashboard_blueprint = Blueprint(
    "dashboard_blueprint", __name__, template_folder="templates", static_folder="static"
)


@dashboard_blueprint.route("/dashboard", methods=["GET", "POST"])
# @login_required
def dashboard():
    
    return render_template("dashboard.html")
