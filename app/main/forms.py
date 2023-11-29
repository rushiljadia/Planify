from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    StringField,
    TimeField,
    SubmitField,
    SelectField,
    SelectMultipleField,
    widgets,
    RadioField,
    BooleanField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    StopValidation,
    Optional,
    InputRequired,
)


def get_places():
    places = {
        "Atkins Library": {
            "code": "ATKNS",
            "address": "9201 University City Blvd, Charlotte, NC 28223",
        },
        "Barnard": {
            "code": "BRNRD",
            "address": "9129 Mary Alexander Rd, Charlotte, NC 28223",
        },
        "Belk Gym": {
            "code": "GYMNS",
            "address": "8911 University Rd, Charlotte, NC 28223",
        },
        "Bioinformatics": {
            "code": "BION",
            "address": "9331 Robert D. Snyder Rd, Charlotte, NC 28223",
        },
        "Burson": {
            "code": "BURSN",
            "address": "9006 Craver Rd, Charlotte, NC 28223",
        },
        "Cameron": {
            "code": "CARC",
            "address": "9010 Craver Rd, Charlotte, NC 28223",
        },
        "Cato College of Education": {
            "code": "COED",
            "address": "8838 Craver Rd, Charlotte, NC 28223",
        },
        "College of Health and Human Services": {
            "code": "CHHS",
            "address": "8844 Craver Rd, Charlotte, NC 28223",
        },
        "Colvard": {
            "code": "COLVD",
            "address": "9105 University Rd, Charlotte, NC 28223",
        },
        "Bonnie E. Cone Center": {
            "code": "CONE",
            "address": "9025 University Rd, Charlotte, NC 28223",
        },
        "Denny": {
            "code": "DENNY",
            "address": "9125 Mary Alexander Rd, Charlotte, NC 28223",
        },
        "Duke Centennial": {
            "code": "DUKE",
            "address": "9330 Robert D. Snyder Rd, Charlotte, NC 28223",
        },
        "Energy Production and Infrastructure Center": {
            "code": "EPIC",
            "address": "8700 Phillips Rd, Charlotte, NC 28262",
        },
        "Fretwell": {
            "code": "FRET",
            "address": "9203 Mary Alexander Rd, Charlotte, NC 28223",
        },
        "Friday": {
            "code": "FRIDY",
            "address": "9209 Mary Alexander Rd, Charlotte, NC 28262",
        },
        "Garinger": {
            "code": "GRNGR",
            "address": "9121 Mary Alexander Rd, Charlotte, NC 28223",
        },
        "Kennedy": {
            "code": "KNNDY",
            "address": "9214 South Library Ln, Charlotte, NC 28223",
        },
        "Macy": {
            "code": "MACY",
            "address": "9224 Library Ln, Charlotte, NC 28223",
        },
        "McEniry": {
            "code": "MCEN",
            "address": "9215 Mary Alexander Rd, Charlotte, NC 28223",
        },
        "Popp Martin Student Union": {
            "code": "STUN",
            "address": "8845 Craver Rd, Charlotte, NC 28262",
        },
        "Robinson": {
            "code": "ROBIN",
            "address": "9027 Mary Alexander Rd, Charlotte, NC 28223",
        },
        "Rowe Arts": {
            "code": "ROWE",
            "address": "9119 University Rd, Charlotte, NC 28223",
        },
        "Science": {
            "code": "SCIENC",
            "address": "9029 Craver Rd, Charlotte, NC 28223",
        },
        "Smith": {
            "code": "SMITH",
            "address": "319 Library Ln, Charlotte, NC 28223",
        },
        "Storrs": {
            "code": "STORR",
            "address": "9115 Mary Alexander Rd, Charlotte, NC 28262",
        },
        "Winningham": {
            "code": "WINN",
            "address": "9236 SOUTH Library Ln, Charlotte, NC 28223",
        },
        "Woodward": {
            "code": "WOODW",
            "address": "8723 Cameron Blvd, Charlotte, NC 28262",
        },
    }
    return places.keys()


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MultiCheckboxAtLeastOne:
    def __init__(self, message=None):
        if not message:
            message = "At least one option must be selected."
        self.message = message

    def __call__(self, form, field):
        if len(field.data) == 0:
            raise StopValidation(self.message)


class RequiredIf(InputRequired):
    # a validator which makes a field required if
    # another field is set and has a truthy value

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)


class AddCourseForm(FlaskForm):
    course_code = StringField(
        "Course Code", validators=[DataRequired(), Length(min=4, max=4)]
    )
    course_number = IntegerField(
        "Class Number", validators=[DataRequired(), Length(min=4, max=4)]
    )
    place = SelectField(
        "Course Location", choices=get_places, validators=[DataRequired()]
    )

    choices = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    days = MultiCheckboxField(
        "Class Days", choices=choices, validators=[MultiCheckboxAtLeastOne()]
    )
    # Course Lab Section
    has_lab = BooleanField(
        "Does this class have a lab?", render_kw={"onclick": "disableFormFields()"}
    )
    lab_day = SelectField(
        "Lab Day",
        choices=choices,
        render_kw={"disabled": "true"},
        validators=[RequiredIf("has_lab")],
    )
    lab_start_time = TimeField(
        "Lab start time",
        render_kw={"disabled": "true"},
        validators=[RequiredIf("has_lab")],
    )
    lab_end_time = TimeField(
        "Lab End Time",
        render_kw={"disabled": "true"},
        validators=[RequiredIf("has_lab")],
    )

    start_time = TimeField("Start Time", validators=[DataRequired()])
    end_time = TimeField("End Time", validators=[DataRequired()])
    add_course = SubmitField("Add Class")
