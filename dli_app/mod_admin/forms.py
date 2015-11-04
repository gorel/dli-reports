"""Forms for the admin module

Author: Logan Gore
This file lists all forms to be filled out from within the admin module.
"""

from flask_wtf import (
    Form,
)

from wtforms import (
    HiddenField,
    SelectField,
    TextField,
    TextAreaField,
    validators,
)

from dli_app.mod_admin.models import (
    ErrorReport,
)

from dli_app.mod_auth.models import (
    Department,
    Location,
    RegisterCandidate,
    User,
)

from dli_app.mod_reports.models import (
    Field,
    FieldType,
)


class AddLocationForm(Form):
    """Form for adding a new location"""
    def __init__(self, *args, **kwargs):
        """Initialize an AddLocationForm"""
        Form.__init__(self, *args, **kwargs)
        self.location = None

    def validate(self):
        """Validate the form"""
        res = True
        if not Form.validate(self):
            res = False

        self.location = Location(self.name.data)
        return res

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

        self.department = Department(self.name.data)
        return True

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

        ftype = FieldType.query.get(self.field_type.data)
        if ftype is None:
            self.field_type.errors.append("Field type not found")
            return False

        department = Department.query.get(self.department.data)
        if department is None:
            self.department.errors.append("Department not found")
            return False

        self.field = Field(
            name=self.name.data,
            ftype=ftype,
            department=department,
        )

        return True

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
        coerce=int,
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
        coerce=int,
    )


class AddUserForm(Form):
    """Form for inviting a new user to the site"""
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form"""

        # First make sure we ignore any case differences
        self.email.data = self.email.data.lower()
        self.confirm_email.data = self.confirm_email.data.lower()

        if not Form.validate(self):
            return False

        self.user = RegisterCandidate(email=self.email.data)

        return True

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


class ErrorReportForm(Form):
    """A form for submitting site error reports"""
    def __init__(self, *args, **kwargs):
        """Inititalize the ErrorReportForm"""
        Form.__init__(self, *args, **kwargs)
        self.error_report = None

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

        user = User.query.get(int(self.user_id.data))
        if not user:
            self.user_id.errors.append('Something went wrong internally. Please try again later.')
            return False

        self.error_report = ErrorReport(
            error_text=self.error.data,
            user_text=self.textbox.data,
            is_bug=bool(self.report_type.data),
            user=user,
        )
        return True

    report_type = SelectField(
        'Is this a bug?',
        choices=[
            (1, "Yes, I'm reporting a bug"),
            (0, "No, I'm asking for a feature"),
        ],
        coerce=int,
        validators=[validators.InputRequired()],
    )

    error = HiddenField()
    user_id = HiddenField()

    textbox = TextAreaField(
        'Description',
        validators=[validators.Required()],
    )
