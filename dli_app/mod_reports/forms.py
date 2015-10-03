"""Forms for the reports module

Author: Logan Gore
This file lists all forms to be filled out from within the reports module.
"""

from flask_wtf import (
    Form,
)

from wtforms import (
    DecimalField,
    FieldList,
    HiddenField,
    IntegerField,
    TextField,
    ValidationError,
    validators,
)

from dli_app.mod_reports.models import (
    FieldData,
    FieldTypeConstants,
)


class SplitNumValidator():
    """Custom validator for numbers that need split on a field"""
    def __init__(
        self,
        split='.',
        filter_chars="",
        max_parts=None,
        parts_message=None,
        num_message=None,
    ):
        """Initialize a SplitNumValidator validation object

        Arguments:
        split - The character to split on during validation (default '.')
        max_parts - The maximum number of parts the number can be split into
        parts_message - The error message to display if len(parts) > max_parts
        num_message - The error message to display if part.isdigit() == False
        """

        self.split = split
        self.filter_chars = filter_chars
        self.max_parts = max_parts

        if parts_message is None:
            parts_message = (
                "Field parts must be separated by {split} character'".format(
                    split=self.split,
                )
            )
        self.parts_message = parts_message
        if num_message is None:
            num_message = "{part} is not a number"
        self.num_message = num_message

    def __call__(self, form, field):
        """Call the validation logic"""
        translation_table = {ord(c): None for c in self.filter_chars}
        data = field.data.translate(translation_table)
        if data:
            parts = data.split(self.split)
            if len(parts) > self.max_parts:
                raise ValidationError(self.parts_message)
            for part in parts:
                if not part.isdigit():
                    raise ValidationError(
                        self.num_message.format(
                            part=part,
                        )
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
        self.fields = []
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

    tags = FieldList(TextField('Tag'))


class SubmitReportDataForm(Form):
    """A form for submitting new report data"""

    fields = []
    def __init__(self, *args, **kwargs):
        """Initialize the submit report data form"""
        Form.__init__(self, *args, **kwargs)
        self.data_points = []
        self.stale_values = []
        self.instance_fields = []
        for field in SubmitReportDataForm.fields:
            self.instance_fields.append(field)
        SubmitReportDataForm.fields = []

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

        for field in self.instance_fields:
            formfield = getattr(self, field.name)
            if formfield.data is not None:
                # Check for any old values that should now be deleted
                stale_value = field.data_points.filter_by(
                    ds=self.ds.data,
                ).first()
                if stale_value is not None:
                    self.stale_values.append(stale_value)

                # Create the new data point
                data_point = FieldData(
                    ds=self.ds.data,
                    field=field,
                    value=formfield.data,
                )
                self.data_points.append(data_point)

        return True

    @classmethod
    def get_instance(cls):
        """Return a new class instance of a LocalSubmitReportDataForm"""
        return generate_local_submit_report_data_form()

    ds = HiddenField()

def generate_local_submit_report_data_form():
    """Dynamically generate a specific class for the SubmitReportDataForm"""
    class LocalSubmitReportDataForm(SubmitReportDataForm):
        """Local copy of a SubmitReportDataForm

        Class that represents a specific SubmitReportDataForm
        This is needed because a SubmitReportDataForm only needs fields
        for the user's specific department. It is a massive waste of resources
        to generate each and every field when we know the user will only
        submit the ones related to his or her department. This allows us to
        dynamically load the fields needed for submission DURING run-time.
        """

        def __init__(self, *args, **kwargs):
            """Initialize the local form"""
            SubmitReportDataForm.__init__(self, *args, **kwargs)

        @classmethod
        def add_field(cls, field):
            """Add the given field to this form dynamically"""
            cls.fields.append(field)
            formfield = None
            if field.ftype == FieldTypeConstants.CURRENCY:
                formfield = TextField(
                    field.name,
                    validators=[
                        SplitNumValidator(
                            split='.',
                            filter_chars="$,",
                            max_parts=2,
                            parts_message=(
                                "Currency must be in the format 'dollars.cents'"
                            ),
                        ),
                    ],
                    filters=[lambda x: x or None],
                )
            elif field.ftype == FieldTypeConstants.DOUBLE:
                formfield = DecimalField(
                    field.name,
                    filters=[lambda x: x or None],
                )
            elif field.ftype == FieldTypeConstants.INTEGER:
                formfield = IntegerField(
                    field.name,
                    filters=[lambda x: x or None],
                )
            elif field.ftype == FieldTypeConstants.STRING:
                formfield = TextField(
                    field.name,
                    filters=[lambda x: x or None],
                )
            elif field.ftype == FieldTypeConstants.TIME:
                formfield = TextField(
                    field.name,
                    validators=[
                        SplitNumValidator(
                            split=':',
                            filter_chars="ms",
                            max_parts=2,
                            parts_message=(
                                "Time must be in the format 'min:sec'"
                            ),
                        ),
                    ],
                    filters=[lambda x: x or None],
                )
            setattr(cls, field.name, formfield)

    return LocalSubmitReportDataForm
