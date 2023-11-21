from flask import Blueprint, render_template, request
from flask_wtf import Form
from wtforms import IntegerField, StringField, TimeField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_login import login_required


# Blueprint Configuration
dashboard_blueprint = Blueprint(
    "dashboard_blueprint", __name__, template_folder="templates", static_folder="static"
)


@dashboard_blueprint.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = add_course_form()
    return render_template("dashboard.html", form=form)


@dashboard_blueprint.route("/add-course", methods=["GET", "POST"])
@login_required
def add_course():
    form = add_course_form()
    return render_template("dashboard.html", form=form)


class add_course_form(Form):
    places = [
        {
            "name": "Atkins Library",
            "code": "ATKNS",
            "address": "9201 University City Blvd, Charlotte, NC 28223",
        },
        {
            "name": "Barnard",
            "code": "BRNRD",
            "address": "9129 Mary Alexander Rd, Charlotte, NC 28223",
        },
        {
            "name": "Belk Gym",
            "code": "GYMNS",
            "address": "8911 University Rd, Charlotte, NC 28223",
        },
        {
            "name": "Bioinformatics",
            "code": "BION",
            "address": "9331 Robert D. Snyder Rd, Charlotte, NC 28223",
        },
        {
            "name": "Burson",
            "code": "BURSN",
            "address": "9006 Craver Rd, Charlotte, NC 28223",
        },
        {
            "name": "Cameron",
            "code": "CARC",
            "address": "9010 Craver Rd, Charlotte, NC 28223",
        },
        {
            "name": "Cato College of Education",
            "code": "COED",
            "address": "8838 Craver Rd, Charlotte, NC 28223",
        },
        {
            "name": "College of Health and Human Services",
            "code": "CHHS",
            "address": "8844 Craver Rd, Charlotte, NC 28223",
        },
        {
            "name": "Colvard",
            "code": "COLVD",
            "address": "9105 University Rd, Charlotte, NC 28223",
        },
        {
            "name": "Bonnie E. Cone Center",
            "code": "CONE",
            "address": "9025 University Rd, Charlotte, NC 28223",
        },
        {
            "name": "Denny",
            "code": "DENNY",
            "address": "9125 Mary Alexander Rd, Charlotte, NC 28223",
        },
        {
            "name": "Duke Centennial",
            "code": "DUKE",
            "address": "9330 Robert D. Snyder Rd, Charlotte, NC 28223",
        },
        {
            "name": "Energy Production and Infrastructure Center",
            "code": "EPIC",
            "address": "8700 Phillips Rd, Charlotte, NC 28262",
        },
        {
            "name": "Fretwell",
            "code": "FRET",
            "address": "9203 Mary Alexander Rd, Charlotte, NC 28223",
        },
        {
            "name": "Friday",
            "code": "FRIDY",
            "address": "9209 Mary Alexander Rd, Charlotte, NC 28262",
        },
        {
            "name": "Garinger",
            "code": "GRNGR",
            "address": "9121 Mary Alexander Rd, Charlotte, NC 28223",
        },
        {
            "name": "Kennedy",
            "code": "KNNDY",
            "address": "9214 South Library Ln, Charlotte, NC 28223",
        },
        {
            "name": "Macy",
            "code": "MACY",
            "address": "9224 Library Ln, Charlotte, NC 28223",
        },
        {
            "name": "McEniry",
            "code": "MCEN",
            "address": "9215 Mary Alexander Rd, Charlotte, NC 28223",
        },
        {
            "name": "Popp Martin Student Union",
            "code": "STUN",
            "address": "8845 Craver Rd, Charlotte, NC 28262",
        },
        {
            "name": "Robinson",
            "code": "ROBIN",
            "address": "9027 Mary Alexander Rd, Charlotte, NC 28223",
        },
        {
            "name": "Rowe Arts",
            "code": "ROWE",
            "address": "9119 University Rd, Charlotte, NC 28223",
        },
        {
            "name": "Science",
            "code": "SCIENC",
            "address": "9029 Craver Rd, Charlotte, NC 28223",
        },
        {
            "name": "Smith",
            "code": "SMITH",
            "address": "319 Library Ln, Charlotte, NC 28223",
        },
        {
            "name": "Storrs",
            "code": "STORR",
            "address": "9115 Mary Alexander Rd, Charlotte, NC 28262",
        },
        {
            "name": "Winningham",
            "code": "WINN",
            "address": "9236 SOUTH Library Ln, Charlotte, NC 28223",
        },
        {
            "name": "Woodward",
            "code": "WOODW",
            "address": "8723 Cameron Blvd, Charlotte, NC 28262",
        },
    ]

    course_code = StringField("Course Code", validators=[DataRequired()])
    course_number = IntegerField("Class Number", validators=[DataRequired()])
    place = SelectField("Course Location", choices=places)
    start_time = TimeField("Start Time", validators=[DataRequired()])
    end_time = TimeField("End Time", validators=[DataRequired()])
    add_course = SubmitField("Add Class")
