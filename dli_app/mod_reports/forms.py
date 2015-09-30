"""Forms for the reports module

Author: Logan Gore
This file lists all forms to be filled out from within the reports module.
"""

from flask_wtf import (
    Form,
)

from wtforms import (
    FieldList,
    FormField,
    HiddenField,
    TextField,
    validators,
)


class ReportFieldForm(Form):
    """A form defining a specific field to add to a report"""
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False
        # TODO: Additional validation


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

    user_id = HiddenField()

    name = TextField(
        "Report name",
        validators=[
            validators.Required(
                message="Please give this report a name.",
            ),
        ],
    )

    fields = FieldList(FormField(ReportFieldForm))

    tags = FieldList(TextField('Tag'))


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

