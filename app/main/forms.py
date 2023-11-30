"""Forms for the main functions of the app"""
from typing import Any
from flask_wtf import FlaskForm
from wtforms import (
    Field,
    IntegerField,
    StringField,
    SubmitField,
    SelectField,
    SelectMultipleField,
    TimeField,
    widgets,
    BooleanField,
)
from wtforms.validators import (
    Length,
    StopValidation,
    InputRequired,
    Regexp,
)


def get_places():
    """Holds the possible places that a user could take a class at along with
    the address of the building"""
    places = [
        ("9201 University City Blvd, Charlotte, NC 28223", "Atkins Library"),
        ("9129 Mary Alexander Rd, Charlotte, NC 28223", "Barnard"),
        ("8911 University Rd, Charlotte, NC 28223", "Belk Gym"),
        ("9331 Robert D. Snyder Rd, Charlotte, NC 28223", "Bioinformatics"),
        ("9006 Craver Rd, Charlotte, NC 28223", "Burson"),
        ("9010 Craver Rd, Charlotte, NC 28223", "Cameron"),
        ("8838 Craver Rd, Charlotte, NC 28223", "Cato College of Education"),
        ("8844 Craver Rd, Charlotte, NC 28223", "College of Health and Human Services"),
        ("9105 University Rd, Charlotte, NC 28223", "Colvard"),
        ("9025 University Rd, Charlotte, NC 28223", "Bonnie E. Cone Center"),
        ("9125 Mary Alexander Rd, Charlotte, NC 28223", "Denny"),
        ("9330 Robert D. Snyder Rd, Charlotte, NC 28223", "Duke Centennial"),
        (
            "8700 Phillips Rd, Charlotte, NC 28262",
            "Energy Production and Infrastructure Center",
        ),
        ("9203 Mary Alexander Rd, Charlotte, NC 28223", "Fretwell"),
        ("9209 Mary Alexander Rd, Charlotte, NC 28262", "Friday"),
        ("9121 Mary Alexander Rd, Charlotte, NC 28223", "Garinger"),
        ("9214 South Library Ln, Charlotte, NC 28223", "Kennedy"),
        ("9224 Library Ln, Charlotte, NC 28223", "Macy"),
        ("9215 Mary Alexander Rd, Charlotte, NC 28223", "McEniry"),
        ("8845 Craver Rd, Charlotte, NC 28262", "Popp Martin Student Union"),
        ("9027 Mary Alexander Rd, Charlotte, NC 28223", "Robinson"),
        ("9119 University Rd, Charlotte, NC 28223", "Rowe Arts"),
        ("9029 Craver Rd, Charlotte, NC 28223", "Science"),
        ("319 Library Ln, Charlotte, NC 28223", "Smith"),
        ("9115 Mary Alexander Rd, Charlotte, NC 28262", "Storrs"),
        ("9236 SOUTH Library Ln, Charlotte, NC 28223", "Winningham"),
        ("8723 Cameron Blvd, Charlotte, NC 28262", "Woodward"),
    ]

    return places


class MultiCheckboxField(SelectMultipleField):
    """Helper class to create a multi checkbox for field

    Args:
        SelectMultipleField (): Field for multiple selections
    """

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MultiCheckboxAtLeastOne:
    """Helper function for a validating the multicheckbox field.
    Ensures that the user selects atleast one of the options
    """

    def __init__(self, message=None):
        if not message:
            message = "At least one option must be selected."
        self.message = message

    def __call__(self, form, field):
        if len(field.data) == 0:
            raise StopValidation(self.message)


class RequiredIf(InputRequired):
    """Custom validator that makes a field requires only if another field
    is set and has a true values

    Raises:
        Exception: If there is no such field passed to the validator
    """

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception(f"no field named {self.other_field_name} in form")
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)


class AddCourseForm(FlaskForm):
    """For used to add a class to the database"""

    # Field for the class name
    course_name = StringField(
        "Course Name",
        validators=[
            InputRequired(),
            Length(min=4, max=25),
            Regexp(
                "/^[a-zA-Z\s]*$/",
                message="Course name must only contain letters and spaces",
            ),
        ],
    )

    # Field for the class code
    course_code = StringField(
        "Course Code", validators=[InputRequired(), Length(min=4, max=4)]
    )

    # Field for the class number
    course_number = IntegerField(
        "Class Number", validators=[InputRequired(), Length(min=4, max=4)]
    )

    # Field to select which building the course takes place
    place = SelectField(
        "Course Location", choices=get_places, validators=[InputRequired()]
    )

    choices = [
        ("M", "Monday"),
        ("T", "Tuesday"),
        ("W", "Wednesday"),
        ("R", "Thursday"),
        ("F", "Friday"),
    ]

    # Day selection field
    days = MultiCheckboxField(
        "Class Days", choices=choices, validators=[MultiCheckboxAtLeastOne()]
    )

    # Time that the class starts on each day
    start_time = TimeField("Start Time", format="%H:%M", validators=[InputRequired()])
    # Time that the class ends on each day
    end_time = TimeField("End Time", format="%H:%M", validators=[InputRequired()])

    # Course Lab Section
    has_lab = BooleanField(
        "Does this class have a lab?", render_kw={"onclick": "disableFormFields()"}
    )

    # Day that the lab takes place
    lab_day = SelectField(
        "Lab Day",
        choices=choices,
        render_kw={"disabled": "true"},
        validators=[RequiredIf("has_lab")],
    )
    # Time that the lab starts
    lab_start_time = TimeField(
        "Lab start time",
        render_kw={"disabled": "true"},
        validators=[RequiredIf("has_lab")],
    )
    # Time that the lab ends
    lab_end_time = TimeField(
        "Lab End Time",
        render_kw={"disabled": "true"},
        validators=[RequiredIf("has_lab")],
    )

    add_course = SubmitField("Add Class")
