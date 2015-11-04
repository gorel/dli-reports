"""Forms that don't belong in any specific module

Author: Logan Gore
This file lists all forms to be filled out that don't fit into a module.
"""

from flask_wtf import (
    Form,
)

from wtforms import (
    HiddenField,
    TextAreaField,
    validators,
)

from dli_app.models import (
    ErrorReport,
)


class ErrorReportForm(Form):
    """A form for submitting site error reports"""
    def __init__(self, *args, **kwargs):
        """Inititalize the ErrorReportForm"""
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

        error_report = ErrorReport.query.get(self.error_id.data)
        if not error_report:
            self.textbox.errors.append(
                "Something went wrong internally and your report can't be submitted at this time."
            )
            return False

        error_report.text = self.textbox.data
        return True

    error_id = HiddenField()

    textbox = TextAreaField(
        'Error description',
        validators=[
            validators.Required(),
        ],
    )
