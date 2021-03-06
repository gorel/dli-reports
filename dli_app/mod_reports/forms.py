"""Forms for the reports module

Author: Logan Gore
This file lists all forms to be filled out from within the reports module.
"""

from datetime import datetime

from flask_wtf import Form
from flask_wtf import html5

from wtforms import BooleanField
from wtforms import DecimalField
from wtforms import HiddenField
from wtforms import IntegerField
from wtforms import SelectField
from wtforms import SelectMultipleField
from wtforms import TextField
from wtforms import ValidationError
from wtforms import validators
from wtforms import widgets
from wtforms import Field as FormField

from wtforms.widgets import TextInput

from dli_app.mod_auth.models import Department
from dli_app.mod_auth.models import User

from dli_app.mod_reports.models import Chart
from dli_app.mod_reports.models import ChartType
from dli_app.mod_reports.models import ChartTypeConstants
from dli_app.mod_reports.models import Field
from dli_app.mod_reports.models import FieldData
from dli_app.mod_reports.models import FieldTypeConstants
from dli_app.mod_reports.models import Report
from dli_app.mod_reports.models import Tag


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
        if not num_message:
            num_message = "{part} is not a number"
        self.num_message = num_message

    def __call__(self, form, field):
        """Call the validation logic"""
        if field.data:
            translation_table = {ord(c): None for c in self.filter_chars}
            data = field.data.translate(translation_table)
            if data:
                parts = data.split(self.split)
                if len(parts) > self.max_parts:
                    raise ValidationError(self.parts_message)
                for part in parts:
                    if part and not part.isdigit():
                        raise ValidationError(
                            self.num_message.format(
                                part=part,
                            )
                        )


class ListField(FormField):
    """A special field that can store a list of values
    Different from FieldList in that it doesn't care about order. FieldList
    doesn't work with the well-known `fields[]` syntax that is essentially
    standard in HTML/JS. This doesn't either, but still works with the
    much-easier-to-serialize-to `fields=id1,id2,id3` syntax.
    Author: Jon Egeland
    """

    def __init__(self, *args, **kwargs):
        """Initialize the ListField"""
        FormField.__init__(self, *args, **kwargs)
        self.data = None

    widget = TextInput()

    def _value(self):
        """Get the value of the field"""
        if self.data:
            return unicode(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        """Process the form data for this field"""
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []


class CreateReportForm(Form):
    """A form for creating a new report"""

    def __init__(self, *args, **kwargs):
        """Initialize the create report form"""
        Form.__init__(self, *args, **kwargs)
        self.report = None

    user_id = HiddenField()

    fields = ListField()
    tags = ListField()

    name = TextField(
        "Report name",
        validators=[
            validators.Required(
                message="Please give this report a name.",
            ),
        ],
    )

    @classmethod
    def get_instance(cls):
        """Return a new class instance of a LocalCreateReportForm"""
        return cls.generate_local_create_report_form()

    @classmethod
    def generate_local_create_report_form(cls):
        """Dynamically generate a class for the SubmitReportDataForm"""
        class LocalCreateReportForm(CreateReportForm):
            """Local copy of a CreateReportForm

            This class represents a dynamic CreateReportForm since we don't
            know what fields are available until runtime. Form more info,
            see LocalSubmitReportDataForm below.
            """

            departments = []
            def __init__(self, *args, **kwargs):
                """Initialize the local form"""
                CreateReportForm.__init__(self, *args, **kwargs)
                self.departments = [
                    dept for dept in LocalCreateReportForm.departments
                ]
                LocalCreateReportForm.departments = []

            def validate(self):
                """Validate the form"""
                res = True
                if not Form.validate(self):
                    res = False

                report_fields = Field.query.filter(Field.id.in_([int(f) for f in self.fields.data if f])).all()

                tags = [
                    Tag.get_or_create(tag.strip()) for tag in self.tags.data
                    if tag.strip()
                ]

                user = User.query.get(self.user_id.data)
                if not user:
                    self.user_id.errors.append("User not found!")
                    res = False

                self.report = Report(
                    user=user,
                    name=self.name.data,
                    fields=report_fields,
                    tags=tags,
                )

                return res

            @classmethod
            def add_department(cls, department):
                """Add the given department to this form dynamically"""
                cls.departments.append(department)
                formfield = SelectMultipleField(
                    department.name,
                    choices=[
                        (field.id, field.name) for field in department.fields
                    ],
                    coerce=int,
                    option_widget=widgets.CheckboxInput(),
                    widget=widgets.ListWidget(prefix_label=False),
                )

                setattr(cls, department.name, formfield)

        return LocalCreateReportForm


class CreateChartForm(Form):
    """A form for creating new charts"""

    def __init__(self, *args, **kwargs):
        """Initialize the create chart form"""
        Form.__init__(self, *args, **kwargs)
        self.chart = None

    user_id = HiddenField()

    fields = ListField()
    tags = ListField()

    name = TextField(
        "Chart name",
        validators=[
            validators.Required(
                message="Please give this chart a name.",
            ),
        ],
    )

    chart_type = SelectField(
        "Chart Type",
        coerce=int,
    )

    with_table = BooleanField('Include table?')

    @classmethod
    def get_instance(cls):
        """Return a new class instance of a LocalCreateChartForm"""
        return cls.generate_local_create_chart_form()

    @classmethod
    def generate_local_create_chart_form(cls):
        """Dynamically generate a class for the LocalCreateChartForm"""
        class LocalCreateChartForm(CreateChartForm):
            """Local copy of a CreateChartForm

            This class represents a dynamic CreateChartForm since we don't
            know what fields are available until runtime. Form more info,
            see LocalSubmitReportDataForm.
            """

            departments = []
            def __init__(self, *args, **kwargs):
                """Initialize the local form"""
                CreateChartForm.__init__(self, *args, **kwargs)
                self.departments = [
                    dept for dept in LocalCreateChartForm.departments
                ]
                LocalCreateChartForm.departments = []

            def validate(self):
                """Validate the form"""
                res = True
                if not Form.validate(self):
                    res = False

                chart_fields = Field.query.filter(Field.id.in_([int(f) for f in self.fields.data if f])).all()
                tags = [
                    Tag.get_or_create(tag.strip()) for tag in self.tags.data
                    if tag.strip()
                ]

                user = User.query.get(self.user_id.data)
                if not user:
                    self.user_id.errors.append("User not found!")
                    res = False

                ctype = ChartType.query.get(self.chart_type.data)
                if not ctype:
                    self.chart_type.errors.append("Chart Type not found!")
                    res = False

                if not len(chart_fields):
                    self.with_table.errors.append("You've created an empty chart!")
                    res = False

                if not self.with_table.data and ctype == ChartTypeConstants.TABLE_ONLY:
                    # It's a fair assumption that the user actually wanted a table
                    self.with_table.data = True

                self.chart = Chart(
                    name=self.name.data,
                    with_table=self.with_table.data,
                    user=user,
                    ctype=ctype,
                    fields=chart_fields,
                    tags=tags,
                )

                return res

            @classmethod
            def add_department(cls, department):
                """Add the given department to this form dynamically"""
                cls.departments.append(department)
                formfield = SelectMultipleField(
                    department.name,
                    choices=[
                        (field.id, field.name) for field in department.fields
                    ],
                    coerce=int,
                    option_widget=widgets.CheckboxInput(),
                    widget=widgets.ListWidget(prefix_label=False),
                )

                setattr(cls, department.name, formfield)

        return LocalCreateChartForm


class EditChartForm(Form):
    """A form for editing new charts"""

    def __init__(self, *args, **kwargs):
        """Initialize the edit chart form"""
        Form.__init__(self, *args, **kwargs)
        self.chart = None

    chart_id = HiddenField()

    fields = ListField()
    tags = ListField()

    name = TextField(
        "Chart name",
        validators=[
            validators.Required(
                message="Please give this chart a name.",
            ),
        ],
    )

    chart_type = SelectField(
        "Chart Type",
        coerce=int,
    )

    with_table = BooleanField('Include table?')

    @classmethod
    def get_instance(cls):
        """Return a new class instance of a LocalEditChartForm"""
        return cls.generate_local_edit_chart_form()

    @classmethod
    def generate_local_edit_chart_form(cls):
        """Dynamically generate a class for the LocalEditChartForm"""
        class LocalEditChartForm(EditChartForm):
            """Local copy of a EditChartForm

            This class represents a dynamic EditChartForm since we don't
            know what fields are available until runtime. Form more info,
            see LocalSubmitReportDataForm.
            """

            departments = []
            def __init__(self, *args, **kwargs):
                """Initialize the local form"""
                EditChartForm.__init__(self, *args, **kwargs)
                self.departments = [
                    dept for dept in LocalEditChartForm.departments
                ]
                LocalEditChartForm.departments = []

            def validate(self):
                """Validate the form"""

                if not Form.validate(self):
                    return False

                self.chart = Chart.query.get(self.chart_id.data)

                chart_fields = Field.query.filter(Field.id.in_([int(f) for f in self.fields.data if f])).all()
                tags = [
                    Tag.get_or_create(tag.strip()) for tag in self.tags.data
                    if tag.strip()
                ]

                res = True
                ctype = ChartType.query.get(self.chart_type.data)
                if not ctype:
                    self.chart_type.errors.append("Chart Type not found!")
                    res = False

                self.chart.name = self.name.data
                self.chart.with_table = self.with_table.data
                self.chart.ctype = ctype
                self.chart.fields = chart_fields
                self.chart.tags = tags

                return res

            @classmethod
            def add_department(cls, department):
                """Add the given department to this form dynamically"""
                cls.departments.append(department)
                formfield = SelectMultipleField(
                    department.name,
                    choices=[
                        (field.id, field.name) for field in department.fields
                    ],
                    coerce=int,
                    option_widget=widgets.CheckboxInput(),
                    widget=widgets.ListWidget(prefix_label=False),
                )

                setattr(cls, department.name, formfield)

        return LocalEditChartForm


class SubmitReportDataForm(Form):
    """A form for submitting new report data"""

    ds = HiddenField()

    def __init__(self, *args, **kwargs):
        """Initialize the submit report data form"""
        Form.__init__(self, *args, **kwargs)
        self.data_points = []
        self.stale_values = []

    @classmethod
    def get_instance(cls):
        """Return a new class instance of a LocalSubmitReportDataForm"""
        return cls.generate_local_submit_report_data_form()

    @classmethod
    def generate_local_submit_report_data_form(cls):
        """Dynamically generate a class for the SubmitReportDataForm"""
        class LocalSubmitReportDataForm(SubmitReportDataForm):
            """Local copy of a SubmitReportDataForm

            Class that represents a specific SubmitReportDataForm
            This is needed because a SubmitReportDataForm only needs fields
            for the user's specific department. It is a massive waste of
            resources to generate each and every field when we know the user
            will only submit the ones related to his or her department. This
            allows us to dynamically load the fields needed for submission
            DURING run-time.
            """

            fields = []
            def __init__(self, *args, **kwargs):
                """Initialize the local form"""
                SubmitReportDataForm.__init__(self, *args, **kwargs)
                self.instance_fields = [
                    field for field in LocalSubmitReportDataForm.fields
                ]
                LocalSubmitReportDataForm.fields = []

            def validate(self):
                """Validate the form"""
                res = True
                if not Form.validate(self):
                    res = False

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

                return res

            @classmethod
            def add_field(cls, field):
                """Add the given field to this form dynamically"""
                cls.fields.append(field)
                formfield = None
                FieldTypeConstants.reload()
                if field.ftype == FieldTypeConstants.CURRENCY:
                    formfield = TextField(
                        field.name,
                        validators=[
                            validators.Optional(),
                            SplitNumValidator(
                                split='.',
                                filter_chars="$,",
                                max_parts=2,
                                parts_message=(
                                    "Currency must be in the format "
                                    "'dollars.cents'"
                                ),
                            ),
                        ],
                        filters=[lambda x: x or None],
                    )
                elif field.ftype == FieldTypeConstants.DOUBLE:
                    formfield = DecimalField(
                        field.name,
                        validators=[validators.Optional()],
                        filters=[lambda x: x or None],
                    )
                elif field.ftype == FieldTypeConstants.INTEGER:
                    formfield = IntegerField(
                        field.name,
                        validators=[validators.Optional()],
                        filters=[lambda x: x or None],
                    )
                elif field.ftype == FieldTypeConstants.STRING:
                    formfield = TextField(
                        field.name,
                        validators=[validators.Optional()],
                        filters=[lambda x: x or None],
                    )
                elif field.ftype == FieldTypeConstants.TIME:
                    formfield = TextField(
                        field.name,
                        validators=[
                            validators.Optional(),
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


class ChangeDateForm(Form):
    """Form to change the date when viewing a specific Report"""
    def __init__(self, *args, **kwargs):
        """Initialize the ChangeDateForm object"""
        Form.__init__(self, *args, **kwargs)
        self.ds = None

    def validate(self):
        """Ensure the given date is within reasonable bounds"""
        if not Form.validate(self):
            return False

        if self.date.data > datetime.now().date():
            self.date.errors.append("Error: date is in the future")
            return False

        self.ds = self.date.data.strftime("%Y-%m-%d")
        return True

    date = html5.DateField(
        "Date",
        format="%Y-%m-%d",
    )


class ChangeDateAndDepartmentForm(Form):
    """Form to change the date and/or department of a Report Form"""
    def __init__(self, *args, **kwargs):
        """Initialize the ChangeDateAndDepartmentForm object"""
        Form.__init__(self, *args, **kwargs)
        self.ds = None
        self.dept_id = None
        self.department.choices = [
            (dept.id, dept.name) for dept in Department.query.all()
        ]

    def validate(self):
        """Ensure the given date is within reasonable bounds"""
        if not Form.validate(self):
            return False

        if self.date.data > datetime.now().date():
            self.date.errors.append("Error: date is in the future")
            return False

        self.ds = self.date.data.strftime("%Y-%m-%d")
        self.dept_id = self.department.data
        return True

    date = html5.DateField(
        "Date",
        format="%Y-%m-%d",
    )

    department = SelectField(
        "Department",
        coerce=int,
    )


class EditReportForm(Form):
    """A form for creating a new report"""

    def __init__(self, *args, **kwargs):
        """Initialize the edit report form"""
        Form.__init__(self, *args, **kwargs)
        self.report = None

    report_id = HiddenField()

    name = TextField(
        "Report name",
        validators=[
            validators.Required(
                message="Please give this report a name.",
            ),
        ],
    )

    fields = ListField()
    tags = ListField()

    @classmethod
    def get_instance(cls):
        """Return a new class instance of a LocalEditReportForm"""
        return cls.generate_local_edit_report_form()

    @classmethod
    def generate_local_edit_report_form(cls):
        """Dynamically generate a class for the EditReportDataForm"""
        class LocalEditReportForm(EditReportForm):
            """Local copy of a EditReportForm

            This class represents a dynamic EditReportForm since we don't
            know what fields are available until runtime. For more info,
            see LocalSubmitReportDataForm.
            """

            departments = []
            def __init__(self, *args, **kwargs):
                """Initialize the local form"""
                EditReportForm.__init__(self, *args, **kwargs)
                self.departments = [
                    dept for dept in LocalEditReportForm.departments
                ]
                LocalEditReportForm.departments = []

            def validate(self):
                """Validate the form"""
                if not Form.validate(self):
                    return False

                self.report = Report.query.get(self.report_id.data)

                report_fields = Field.query.filter(Field.id.in_([int(f) for f in self.fields.data if f])).all()
                tags = [
                    Tag.get_or_create(tag.strip()) for tag in self.tags.data
                    if tag.strip()
                ]

                self.report.name = self.name.data
                self.report.fields = report_fields
                self.report.tags = tags

                return True

            @classmethod
            def add_department(cls, department):
                """Add the given department to this form dynamically"""
                cls.departments.append(department)
                formfield = SelectMultipleField(
                    department.name,
                    choices=[
                        (field.id, field.name) for field in department.fields
                    ],
                    coerce=int,
                    option_widget=widgets.CheckboxInput(),
                    widget=widgets.ListWidget(prefix_label=False),
                )

                setattr(cls, department.name, formfield)

        return LocalEditReportForm


class SearchForm(Form):
    """Form to search for a report"""
    REPORTNAME_CHOICE = 0
    OWNER_CHOICE = 1
    EMAIL_CHOICE = 2
    TAG_CHOICE = 3

    def __init__(self, *args, **kwargs):
        """Initialize the SearchForm object"""
        Form.__init__(self, *args, **kwargs)
        self.reports = []

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

        choice = self.filter_choices.data
        search_text = "%{}%".format(self.search_text.data)
        if choice == self.OWNER_CHOICE:
            self.reports = Report.query.join(User, Report.user).filter(User.name.ilike(search_text)).all()
        elif choice == self.EMAIL_CHOICE:
            self.reports = Report.query.join(User, Report.user).filter(User.email.ilike(search_text)).all()
        elif choice == self.REPORTNAME_CHOICE:
            self.reports = Report.query.filter(Report.name.ilike(search_text)).all()
        elif choice == self.TAG_CHOICE:
            self.reports = Report.query.join(Tag, Report.tags).filter(Tag.name.ilike(search_text)).all()
        else:
            self.filter_choices.errors.append('Not a valid choice!')
            return False

        return True

    filter_choices = SelectField(
        "Filter by",
        choices=[
            (REPORTNAME_CHOICE, 'Report Name'),
            (OWNER_CHOICE, 'Owner Name'),
            (EMAIL_CHOICE, 'Owner Email'),
            (TAG_CHOICE, 'Tag')
        ],
        coerce=int,
    )

    search_text = TextField(
        "Search",
    )


class DownloadReportForm(Form):
    """Form to download report data"""
    def __init__(self, *args, **kwargs):
        """Initialize the DownloadReportForm object"""
        Form.__init__(self, *args, **kwargs)
        self.start = None
        self.end = None

    def validate(self):
        """Ensure the given dates are within reasonable bounds"""
        res = True
        if not Form.validate(self):
            res = False

        if self.start_date.data > self.end_date.data:
            self.start_date.errors.append("Start date cannot be after end date")
            res = False

        if res:
            self.start = self.start_date.data.strftime("%Y-%m-%d")
            self.end = self.end_date.data.strftime("%Y-%m-%d")
        return res

    start_date = html5.DateField(
        "Start Date",
        format="%Y-%m-%d",
    )

    end_date = html5.DateField(
        "End Date",
        format="%Y-%m-%d",
    )
