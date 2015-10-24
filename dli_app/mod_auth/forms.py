"""Forms for the auth module

Author: Logan Gore
This file lists all forms to be filled out from within the auth module.
"""

from flask_wtf import (
    Form,
)

from wtforms import (
    BooleanField,
    HiddenField,
    PasswordField,
    SelectField,
    TextField,
    validators,
)

from dli_app.mod_auth.models import (
    Department,
    Location,
    RegisterCandidate,
    User,
)


class RegistrationForm(Form):
    """A form for registering a new user"""
    def __init__(self, *args, **kwargs):
        """Inititalize the registration form"""
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form

        Perform validation by checking that all submitted values are within
        acceptable ranges and the user is allowed to register an account.
        """

        if not Form.validate(self):
            return False

        # First check if the user has already created an account
        user = User.get_by_email(self.email.data)
        if user and user.check_password(self.password.data):
            self.user = user
            return True

        # Check that email is "allowed" to register
        candidate = RegisterCandidate.query.filter_by(
            email=self.email.data,
            registration_key=self.registration_key.data,
        ).first()
        if candidate is None:
            self.email.errors.append(
                "Sorry, you aren't allowed to register at this time.",
            )
            return False

        # Check that location is within list of approved locations
        location = Location.query.get(self.location.data)
        if location is None:
            self.location.errors.append('Location not supported')
            return False

        department = Department.query.get(self.department.data)
        if department is None:
            self.department.errors.append('Department not found')
            return False

        # Create the new user account
        self.user = User(
            name=self.name.data,
            email=self.email.data,
            password=self.password.data,
            location=location,
            department=department,
        )

        return True

    registration_key = HiddenField()

    name = TextField(
        'Full Name',
        validators=[
            validators.Required(
                message='You must provide your full name.',
            ),
        ],
    )

    email = TextField(
        'Email',
        validators=[
            validators.Email(),
            validators.Required(
                message='You must provide your work email address.',
            ),
        ],
    )

    password = PasswordField(
        'Password',
        validators=[
            validators.Required(
                message='Please enter a password.',
            ),
            validators.EqualTo(
                'confirm_password',
                message='Passwords must match',
            ),
        ],
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            validators.Required(
                message='Please confirm your password.',
            ),
        ],
    )

    department = SelectField(
        'Department',
        validators=[
            validators.Required(
                message='Please select your default department.',
            ),
        ],
    )

    location = SelectField(
        'Location',
        validators=[
            validators.Required(
                message='Please enter your default location.',
            ),
        ],
        coerce=int,
    )

    remember = BooleanField(
        'Remember Me?',
    )


class LoginForm(Form):
    """A form for logging in a user"""
    def __init__(self, *args, **kwargs):
        """Inititalize the registration form"""
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form

        Perform validation by checking that the user account exists and the
        password hashes match.
        """
        res = True
        if not Form.validate(self):
            res =  False

        user = User.get_by_email(self.email.data)
        if user is None:
            self.email.errors.append('No account with that email found.')
            res = False

        if not user.check_password(self.password.data):
            self.password.errors.append('Incorrect password!')
            res = False

        self.user = user
        return res

    email = TextField(
        'Email',
        validators=[
            validators.Email(),
            validators.Required(
                message='You must provide your work email address.',
            ),
        ],
    )

    password = PasswordField(
        'Password',
        validators=[
            validators.Required(
                message='Please enter a password.',
            ),
        ],
    )

    remember = BooleanField(
        'Remember Me?',
    )


class ForgotForm(Form):
    """A form for recovering an account with a forgotten password"""

    def validate(self):
        """Validate the form

        Perform validation by checking that the user email exists.
        """

        if not Form.validate(self):
            return False

        user = User.get_by_email(self.email.data)
        if user is None:
            self.email.errors.append('No account with that email found.')
            return False

        self.user = user
        return True

    email = TextField(
        'Email',
        validators=[
            validators.Email(),
            validators.Required(
                message='You must provide your work email address.',
            ),
        ],
    )


class NewPassForm(Form):
    """Form for resetting a user's password"""
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    reset_key = HiddenField()

    password = PasswordField(
        'Password',
        validators=[
            validators.Required(
                message='Please enter a password.',
            ),
            validators.EqualTo(
                'confirm_password',
                message='Passwords must match',
             ),
        ],
    )

    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            validators.Required(
                message='Please confirm your password.',
            ),
        ],
    )

