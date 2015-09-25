"""Forms for the reports module

Author: Logan Gore
This file lists all forms to be filled out from within the reports module.
"""

from wtforms import (
    Form,
)


class CreateReportForm(Form):
    """A form for creating a new report"""
    def __init__(self, *args, **kwargs):
        """Initialize the create report form"""
        Form.__init__(self, *args, **kwargs)
        self.report = None

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False
        # TODO: Additional validation


class SubmitReportDataForm(Form):
    """A form for submitting new report data"""
    def __init__(self, *args, **kwargs):
        """Initialize the submit report data form"""
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False
        # TODO: Additional validation

