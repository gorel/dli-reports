from flask.ext.wtf import (
    Form,
)

from wtforms import (
    BooleanField,
    PasswordField,
    SelectField,
    TextField,
    validators,
)

from dli_app import db

from dli_app.mod_auth.models import (
    Location,
    RegisterCandidate,
    User,
)

class RegistrationForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
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
        ).first()
        if candidate is None:
            self.email.errors.append(
                "Sorry, you aren't allowed to register at this time.",
            )
            return False

        # Check that location is within list of approved locations
        location = Location.get(self.location.data)
        if location is None:
            self.location.errors.append('Location not supported')
            return False

        # Create the new user account and add it to the db
        self.user = User(
            name=self.name.data,
            email=self.email.data,
            password=self.password.data,
            location=location,
        )

        db.session.add(self.user)
        db.session.commit()

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
    def __init__(Form, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.get_by_email(self.email.data)
        if user is None:
            self.email.errors.append('No account with that email found.')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Incorrect password!')
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
    email = TextField(
        'Email',
        validators=[
            validators.Email(),
            validators.Required(
                message='You must provide your work email address.',
            ),
        ],
    )
