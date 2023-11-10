from flask import Blueprint, render_template

# Blueprint Configuration
home_blueprint = Blueprint(
    "home_blueprint", __name__, template_folder="templates", static_folder="static"
)


# Home page
@home_blueprint.route("/")
def home():
    """Homepage"""
    return render_template("home.html")
