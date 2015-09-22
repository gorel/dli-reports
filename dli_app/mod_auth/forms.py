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

class RegistrationForm(Form):
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

class LoginForm(Form):
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
