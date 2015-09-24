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

from dli_app.mod_reports.models import (
    Field,
    FieldData,
    FieldType,
    Report,
    Tag,
)

class CreateReportForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        # TODO: Additional validation

class SubmitReportDataForm(Form):
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        # TODO: Additional validation

