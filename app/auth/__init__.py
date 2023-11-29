"""Blueprint for all authentication views"""
from flask import Blueprint

auth = Blueprint("auth", __name__)

from . import views
