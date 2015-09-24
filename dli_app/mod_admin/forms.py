from flask.ext.wtf import (
    Form,
)

from wtforms import (
    PasswordField,
    SelectField,
    TextField,
    validators,
)

class AddLocationForm(Form):
    name = TextField(
        "Location Name",
        validators=[
            validators.Required(
                message='You must provide the name of the location.',
        ],
    )

class AddDepartmentForm(Form):
    name = TextField(
        "Department Name",
        validators=[
            validators.Required(
                message='You must provide the name of the department.',
        ],
    )

class AddFieldForm(Form):
    name = TextField(
        "Field Name",
        validators=[
            validators.Required(
                message='You must provide the name of the field.',
            ),
        ],
    )

    field_type = SelectField(
        "Field Type",
        validators=[
            validators.Required(
                message='You must provide the type of the field.',
            ),
        ],
    ),

    department = SelectField(
        'Department',
        validators=[
            validators.Required(
                message=(
                    'Please enter the department that should'
                    'fill out this field by default.'
                ),
            ),
        ],
    )

class AddUserForm(Form):
    name = TextField(
        "Full Name",
        validators=[
            validators.Required(
                message='You must provide the full name of the new user.',
        ],
    )

    email = TextField(
        'Email',
        validators=[
            validators.Email(),
            validators.Required(
                message='You must provide your school email address.',
            ),
            validators.EqualTo(
                'confirm_email',
                message='Emails must match',
            ),
        ],
    )

    confirm_email = TextField(
        'Confirm Email',
        validators=[
            validators.Email(),
            validators.Required(
                message='Please confirm your email address.',
            ),
        ],
    )
