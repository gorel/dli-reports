"""Forms for the admin module

Author: Logan Gore
This file lists all forms to be filled out from within the admin module.
"""

from flask_wtf import (
    Form,
)

from wtforms import (
    SelectField,
    TextField,
    validators,
)


class AddLocationForm(Form):
    """Form for adding a new location"""
    def __init__(self, *args, **kwargs):
        """Initialize an AddLocationForm"""
        Form.__init__(self, *args, **kwargs)
        self.location = None

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

    name = TextField(
        "Location Name",
        validators=[
            validators.Required(
                message='You must provide the name of the location.',
            ),
        ],
    )


class AddDepartmentForm(Form):
    """Form for adding a new department"""
    def __init__(self, *args, **kwargs):
        """Initialize an AddDepartmentForm"""
        Form.__init__(self, *args, **kwargs)
        self.department = None

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

    name = TextField(
        "Department Name",
        validators=[
            validators.Required(
                message='You must provide the name of the department.',
            ),
        ],
    )


class AddFieldForm(Form):
    """Form for adding a new field to a department"""
    def __init__(self, *args, **kwargs):
        """Initialize an AddFieldForm"""
        Form.__init__(self, *args, **kwargs)
        self.field = None

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

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
    )

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
    """Form for inviting a new user to the site"""
    def __init__(self, *args, **kwargs):
        """Initialize the AddUserForm"""
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

    name = TextField(
        "Full Name",
        validators=[
            validators.Required(
                message='You must provide the full name of the new user.',
            ),
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
