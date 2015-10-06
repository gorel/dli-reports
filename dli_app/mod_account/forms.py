"""Forms for the account module

Author: Logan Gore
This file lists all forms to be filled out from within the account module.
"""

from flask_wtf import (
    Form,
)

from wtforms import (
    HiddenField,
    PasswordField,
    SelectField,
    TextField,
    validators,
)

from dli_app.mod_auth.models import (
    Department,
    Location,
    User,
)


class EditAccountForm(Form):
    """A form for editing the details of a User's account"""
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

        user = User.query.get(self.user_id.data)
        if user is None:
            self.user_id.errors.append('User not found')
            return False

        location = Location.query.get(self.location.data)
        if location is None:
            self.location.errors.append('Location not found')
            return False

        department = Department.query.get(self.department.data)
        if department is None:
            self.department.errors.append('Department not found')

        # Set all of the values now that validation is complete
        user.name = self.name.data or user.name
        user.location = location
        user.department = department

        if self.password.data:
            user.set_password(self.password.data)


    user_id = HiddenField()

    name = TextField('Full Name')

    password = PasswordField(
        'Password',
        validators=[
            validators.EqualTo(
                'confirm_password',
                message='Passwords must match',
            ),
        ],
    )

    confirm_password = PasswordField('Confirm Password')

    location = SelectField(
        "Location",
        validators=[
            validators.Required(
                message='Please enter your location.',
            ),
        ],
        coerce=int,
    )

    department = SelectField(
        "Department",
        validators=[
            validators.Required(
                message='Please enter your default department.',
            ),
        ],
        coerce=int,
    )
