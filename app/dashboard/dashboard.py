from flask import Blueprint, render_template
from flask_login import login_required

# Blueprint Configuration
dashboard_blueprint = Blueprint(
    "dashboard_blueprint", __name__, template_folder="templates", static_folder="static"
)


@dashboard_blueprint.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html")
