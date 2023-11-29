from . import main
from flask import render_template


@main.app_errorhandler(404)
def page_not_found(e):
    """Used for redirecting to a 404 erro page"""
    return render_template("errors/404.html"), 404
