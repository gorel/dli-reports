"""Models for the reports module

Author: Logan Gore
This file is responsible for defining models that belong in the reports module.
"""

import collections
import datetime
import os

import xlsxwriter

from dli_app import db

EXCEL_FILE_DIR = "excel-files"

report_fields = db.Table(
    'report_fields',
    db.Column('report_id', db.Integer, db.ForeignKey('report.id')),
    db.Column('field_id', db.Integer, db.ForeignKey('field.id')),
)


report_tags = db.Table(
    'report_tags',
    db.Column('report_id', db.Integer, db.ForeignKey('report.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
)


chart_fields = db.Table(
    'chart_fields',
    db.Column('chart_id', db.Integer, db.ForeignKey('chart.id')),
    db.Column('field_id', db.Integer, db.ForeignKey('field.id')),
)


chart_tags = db.Table(
    'chart_tags',
    db.Column('chart_id', db.Integer, db.ForeignKey('chart.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
)


class Tag(db.Model):
    """Model for a Tag associated with a Report"""
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __init__(self, name):
        """Initialize a Tag model"""
        self.name = name

    def __repr__(self):
        """Return a descriptive representation of a Tag"""
        return '<Tag %r>' % self.name

    @classmethod
    def get_or_create(cls, name):
        """Either retrieve a tag or create it if it doesn't exist"""
        tag = Tag.query.filter_by(name=name).first()
        if tag is None:
            tag = Tag(name)
            db.session.add(tag)
            db.session.commit()
        return tag


class FieldType(db.Model):
    """Model for the type of a Field"""
    __tablename__ = "field_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)

    def __init__(self, name):
        """Initialize a FieldType model"""
        self.name = name

    def __repr__(self):
        """Return a descriptive representation of a FieldType"""
        return '<Field Type %r>' % self.name

    def __eq__(self, other):
        """Determine if two FieldTypes are equal"""
        return other is not None and self.id == other.id


class FieldData(db.Model):
    """Model for the actual data stored in a Field"""
    __tablename__ = "field_data"
    id = db.Column(db.Integer, primary_key=True)
    ds = db.Column(db.String(16))
    field_id = db.Column(db.Integer, db.ForeignKey("field.id"))
    ivalue = db.Column(db.BigInteger)
    dvalue = db.Column(db.Float)
    svalue = db.Column(db.String(128))

    def __init__(self, ds, field, value):
        """Initialize a FieldData model"""
        self.ds = ds
        self.field = field

        # Type checking should have already been done from the form
        if self.field.ftype == FieldTypeConstants.CURRENCY:
            parts = value.replace(',', '').replace('$', '').split('.')
            # Convert the value into cents to avoid any floating-point issues
            self.ivalue = int(parts[0]) * 100
            if len(parts) == 2:
                self.ivalue += int(parts[1])
        elif self.field.ftype == FieldTypeConstants.DOUBLE:
            self.dvalue = value
        elif self.field.ftype == FieldTypeConstants.INTEGER:
            self.ivalue = value
        elif self.field.ftype == FieldTypeConstants.STRING:
            self.svalue = value
        elif self.field.ftype == FieldTypeConstants.TIME:
            # Convert the value into seconds for convenience
            parts = value.split(':')
            self.ivalue = int(parts[0]) * 60
            if len(parts) == 2:
                self.ivalue += int(parts[1])

    def __repr__(self):
        """Return a descriptive representation of a FieldData"""
        return '<FieldData of %r>' % self.field.name

    @property
    def value(self):
        """Property to easily retrieve the FieldData's value"""
        ftype = self.field.ftype
        if ftype == FieldTypeConstants.CURRENCY:
            return float(self.ivalue) / 100
        elif ftype == FieldTypeConstants.DOUBLE:
            return self.dvalue
        elif ftype == FieldTypeConstants.INTEGER:
            return self.ivalue
        elif ftype == FieldTypeConstants.STRING:
            return self.svalue
        elif ftype == FieldTypeConstants.TIME:
            return self.ivalue
        else:
            raise NotImplementedError("ERROR: Type %s not supported!" % ftype)

    @property
    def pretty_value(self):
        """Property to easily retrieve a human-readable FieldData model"""
        ftype = self.field.ftype
        if ftype == FieldTypeConstants.CURRENCY:
            dollars = self.ivalue / 100
            cents = self.ivalue % 100
            return "${dollars}.{cents:02d}".format(
                dollars=dollars,
                cents=cents,
            )
        elif ftype == FieldTypeConstants.DOUBLE:
            return str(self.dvalue)
        elif ftype == FieldTypeConstants.INTEGER:
            return str(self.ivalue)
        elif ftype == FieldTypeConstants.STRING:
            return self.svalue
        elif ftype == FieldTypeConstants.TIME:
            mins = self.ivalue / 60
            secs = self.ivalue % 60
            return "{mins}:{secs:02d}".format(
                mins=mins,
                secs=secs,
            )
        else:
            raise NotImplementedError("ERROR: Type %s not supported!" % ftype)


class Field(db.Model):
    """Model for a Field within a Report"""
    __tablename__ = "field"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    ftype_id = db.Column(db.Integer, db.ForeignKey("field_type.id"))
    ftype = db.relationship(FieldType)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    data_points = db.relationship(
        FieldData,
        backref='field',
        lazy='dynamic',
    )

    def __init__(self, name, ftype, department):
        """Initialize a Field model"""
        self.name = name
        self.ftype = ftype
        self.department = department

    def __repr__(self):
        """Return a descriptive representation of a Field"""
        return '<Field %r>' % self.name

    def get_data_for_date(self, ds, pretty=False):
        """Retrieve the FieldData instance for the given date stamp"""
        data_point = self.data_points.filter_by(ds=ds).first()
        if pretty:
            if data_point is not None:
                data_point = data_point.pretty_value
            else:
                data_point = ""
        return data_point

    @property
    def identifier(self):
        """Property to uniquely identify this Field"""
        return '{}: {}'.format(self.department.name, self.name)


class Report(db.Model):
    """Model for a DLI Report"""
    __tablename__ = "report"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    name = db.Column(db.String(128))
    fields = db.relationship(
        Field,
        secondary=report_fields,
        backref='reports',
    )
    tags = db.relationship(
        Tag,
        secondary=report_tags,
        backref='reports',
    )

    def __init__(self, user, name, fields, tags):
        """Initialize a Report model"""
        self.user = user
        self.name = name
        self.fields = fields
        self.tags = tags

    def __repr__(self):
        """Return a descriptive representation of a Report"""
        return '<Report %r>' % self.name

    @property
    def tagnames(self):
        """Helper function to get the names of the Report's tags"""
        return [tag.name for tag in self.tags]

    def generate_filename(self, ds):
        """Generate the filename for the Excel sheet for downloads"""
        return "{filename}-{ds}.xlsx".format(
            filename=self.name,
            ds=ds,
        )

    def collect_dept_data_for_template(self, ds):
        """Collect all of the department data for this Report

        Collect department data for this Report on a given day in a format
        that is easy to template for render_template functions in Jinja2
        """

        dept_data = collections.defaultdict(list)
        for field in self.fields:
            dept_data[field.department.name].append(
                {
                    'name': field.name,
                    'value': field.get_data_for_date(ds, pretty=True),
                }
            )
        return dept_data

    def excel_filepath_for_ds(self, ds):
        """Return the absolute filepath for the Excel sheet on the given ds"""
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            EXCEL_FILE_DIR,
            self.generate_filename(ds),
        )

    def excel_file_exists(self, ds):
        """Determine whether or not an Excel file for this ds exists"""
        return os.path.exists(self.excel_filepath_for_ds(ds))

    def create_excel_file(self, ds):
        """Generate an Excel sheet with this Report's data

        Arguments:
        ds - Date stamp for which day of Report data to generate
        """

        excel_helper = ExcelSheetHelper(
            filepath=self.excel_filepath_for_ds(ds),
            report_name=self.name,
            ds=ds,
        )
        excel_helper.write(self.collect_dept_data(ds))
        excel_helper.finalize()

    def remove_excel_file(self, ds):
        """Delete the Excel file for the given ds"""
        os.remove(self.excel_filepath_for_ds(ds))

    def collect_dept_data(self, ds):
        """Collect all of the department data for this Report"""
        dept_data = collections.defaultdict(list)
        for field in self.fields:
            dept_data[field.department.name].append(
                field.get_data_for_date(ds)
            )
        return dept_data


class ChartType(db.Model):
    """Model for a ChartType (eg. Line, Bar, etc.)"""
    __tablename__ = 'chart_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)

    def __init__(self, name):
        """Initialize a ChartType model"""
        self.name = name

    def __repr__(self):
        """Return a descriptive representation of a ChartType"""
        return '<Chart Type %r>' % self.name

    def __eq__(self, other):
        """Determine if two ChartTypes are equal"""
        return other is not None and self.id == other.id


class ChartDateType(db.Model):
    """Model for a ChartDateType (eg. From week, rolling week, etc.)"""
    __tablename__ = 'chart_date_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)

    def __init__(self, name):
        """Initialize a ChartDateType model"""
        self.name = name

    def __repr__(self):
        """Return a descriptive representation of a ChartDateType"""
        return '<Chart Date Type %r>' % self.name

    def __eq__(self, other):
        """Determine if two ChartDateTypes are equal"""
        return other is not None and self.id == other.id

    @property
    def pretty_value(self):
        """Return a more human-readable representation of this ChartDateType"""
        if self == ChartDateTypeConstants.TODAY:
            return 'Data from today only'
        elif self == ChartDateTypeConstants.FROM_WEEK:
            return 'Data submitted since Sunday'
        elif self == ChartDateTypeConstants.ROLLING_WEEK:
            return 'Data submitted in the last 7 days'
        elif self == ChartDateTypeConstants.FROM_MONTH:
            return 'Data submitted since the first of the month'
        elif self == ChartDateTypeConstants.ROLLING_MONTH:
            return 'Data submitted in the last 30 days'
        elif self == ChartDateTypeConstants.FROM_YEAR:
            return 'Data submitted since January 1st'
        elif self == ChartDateTypeConstants.ROLLING_YEAR:
            return 'Data submitted in the last 365 days'


class Chart(db.Model):
    """Model for a DLI Chart"""
    __tablename__ = "chart"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    with_table = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    ctype_id = db.Column(db.Integer, db.ForeignKey("chart_type.id"))
    ctype = db.relationship(ChartType, backref="charts")
    cdtype_id = db.Column(db.Integer, db.ForeignKey("chart_date_type.id"))
    cdtype = db.relationship(ChartDateType, backref="charts")
    fields = db.relationship(
        Field,
        secondary=chart_fields,
        backref='charts',
    )
    tags = db.relationship(
        Tag,
        secondary=chart_tags,
        backref='charts',
    )

    def __init__(self, name, with_table, user, ctype, cdtype, fields, tags):
        """Initialize a Chart model"""
        self.name = name
        self.with_table = with_table
        self.user = user
        self.ctype = ctype
        self.cdtype = cdtype
        self.fields = fields
        self.tags = tags

    def __repr__(self):
        """Return a descriptive representation of a Chart"""
        return '<Chart %r>' % self.name

    def get_min_date(self):
        """Retrieve the min_ds for this Chart's date range"""
        today = datetime.date.today()
        if self.cdtype == ChartDateTypeConstants.TODAY:
            date = today
        elif self.cdtype == ChartDateTypeConstants.FROM_WEEK:
            days = today.weekday() + 1
            date = today - datetime.timedelta(days=days)
        elif self.cdtype == ChartDateTypeConstants.ROLLING_WEEK:
            date = today - datetime.timedelta(days=7)
        elif self.cdtype == ChartDateTypeConstants.FROM_MONTH:
            date = datetime.date(today.year, today.month, 1)
        elif self.cdtype == ChartDateTypeConstants.ROLLING_MONTH:
            date = today - datetime.timedelta(days=30)
        elif self.cdtype == ChartDateTypeConstants.FROM_YEAR:
            date = datetime.date(today.year, 1, 1)
        elif self.cdtype == ChartDateTypeConstants.ROLLING_YEAR:
            date = today - datetime.timedelta(days=365)
        else:
            raise NotImplementedError('Unexpected cdtype: %r' % self.cdtype)

        return date

    def data_points(self, min_date):
        """Retrieve the data points needed for this chart"""
        min_ds = min_date.strftime('%Y-%m-%d')

        return {
            field.identifier: {
                str(fdata.ds): fdata.value
                for fdata in field.data_points.filter(FieldData.ds >= min_ds)
            }
            for field in self.fields
        }

    @property
    def tagnames(self):
        """Helper function to get the names of the Report's tags"""
        return [tag.name for tag in self.tags]

    def generated_js(self):
        """Property that represents this chart generated as C3 JavaScript"""
        min_date = self.get_min_date()
        generate = 'true'
        if self.ctype == ChartTypeConstants.TABLE_ONLY:
            generate = 'false'

        return """
            var data_points = {data_points};
            var time_series = {time_series};
            var chart_type = "{chart_type}";
            var generate = {should_generate};
        """.format(
            time_series=self.get_time_series_sequence(min_date),
            data_points=self.data_points(min_date),
            chart_type=self.ctype.name,
            should_generate=generate,
        )

    def get_time_series_sequence(self, min_date):
        """Get the time series data that represents this chart in C3"""
        # Any point will do, so just take the first
        today = datetime.date.today()
        days = (today - min_date).days + 1
        ds_list = [min_date + datetime.timedelta(days=x) for x in range(0, days)]
        return [x.strftime('%Y-%m-%d') for x in ds_list]


class ExcelSheetHelper():
    """Helper class to write data to an Excel Sheet for DLI Reports

    Provides functions that write all Report data to an Excel file.
    Overloads the write method to write data while keeping track of the sheet's
    row and column information.
    """

    def __init__(self, filepath, report_name, ds):
        """Initialize an ExcelSheetHelper by creating an XLSX Workbook"""
        self.report_name = report_name
        self.ds = ds

        self.workbook = xlsxwriter.Workbook(filepath)
        self.worksheet = self.workbook.add_worksheet()
        # Set default width of columns A and B a bit wider
        self.worksheet.set_column('A:B', 20)
        self.finalized = False
        self.row = 0
        self.col = 0

        self.title_format = self.workbook.add_format(
            {'bold': True, 'font_size': 36}
        )
        self.report_name_format = self.workbook.add_format(
            {'bold': True, 'font_size': 28}
        )
        self.ds_format = self.workbook.add_format(
            {'font_size': 20}
        )
        self.dept_title_format = self.workbook.add_format(
            {'bold': True, 'font_size': 20}
        )
        self.field_format = self.workbook.add_format({'bold': True})
        self.currency_format = self.workbook.add_format(
            {'num_format': '$#,##0.00;[Red]($#,##0.00)'}
        )
        self.double_format = self.workbook.add_format(
            {'num_format': '0.000'}
        )
        self.integer_format = self.workbook.add_format(
            {'num_format': '0'}
        )
        self.string_format = self.workbook.add_format(
            # No special formatting needed
        )
        self.time_format = self.workbook.add_format(
            {'num_format': 'h:mm'}
        )

        self.initialize_worksheet()

    def initialize_worksheet(self):
        """Write the DLI title and report name on the page"""
        self.worksheet.write(
            self.row,
            self.col,
            "DLI Auto-generated Reports",
            self.title_format,
        )
        self.row += 1

        self.worksheet.write(
            self.row,
            self.col,
            "Report: {name}".format(name=self.report_name),
            self.report_name_format,
        )
        self.row += 1

        self.worksheet.write(
            self.row,
            self.col,
            "Data for {ds}".format(ds=self.ds),
            self.ds_format,
        )
        self.row += 1

    def write(self, dept_data):
        """Write all of the department data for a Report"""
        for dept in dept_data.keys():
            self.write_dept_title(dept)
            for field in dept_data[dept]:
                self.write_field_data(field)

    def write_dept_title(self, dept_name):
        """Write a Department title within a Report"""
        self.row += 1
        self.worksheet.write(
            self.row,
            self.col,
            dept_name,
            self.dept_title_format,
        )
        self.row += 1

    def write_field_data(self, field_data):
        """Write a Field within a Report"""
        self.worksheet.write(
            self.row,
            self.col,
            field_data.field.name,
            self.field_format,
        )
        self.col += 1

        self.worksheet.write(
            self.row,
            self.col,
            field_data.value,
            self.get_format(field_data.field),
        )
        self.row += 1
        self.col = 0

    def get_format(self, field):
        """Get the format required for the specific field"""
        if field.ftype == FieldTypeConstants.CURRENCY:
            return self.currency_format
        elif field.ftype == FieldTypeConstants.DOUBLE:
            return self.double_format
        elif field.ftype == FieldTypeConstants.INTEGER:
            return self.integer_format
        elif field.ftype == FieldTypeConstants.STRING:
            return self.string_format
        elif field.ftype == FieldTypeConstants.TIME:
            return self.time_format

    def finalize(self):
        """Complete the workbook by closing it"""
        if not self.finalized:
            self.workbook.close()
            self.finalized = True


class FieldTypeConstants():
    """Constant FieldTypes used for easy type-checking in other modules"""
    try:
        CURRENCY = FieldType.query.filter_by(name="currency").first()
        DOUBLE = FieldType.query.filter_by(name="double").first()
        INTEGER = FieldType.query.filter_by(name="integer").first()
        STRING = FieldType.query.filter_by(name="string").first()
        TIME = FieldType.query.filter_by(name="time").first()
    except:
        CURRENCY = None
        DOUBLE = None
        INTEGER = None
        STRING = None
        TIME = None

    def __init__(self):
        """Initialize a FieldTypeConstants instance"""
        self.CURRENCY = FieldType.query.filter_by(name="currency").first()
        self.DOUBLE = FieldType.query.filter_by(name="double").first()
        self.INTEGER = FieldType.query.filter_by(name="integer").first()
        self.STRING = FieldType.query.filter_by(name="string").first()
        self.TIME = FieldType.query.filter_by(name="time").first()

    @classmethod
    def reload(cls):
        """Reload the class constants"""
        cls.CURRENCY = FieldType.query.filter_by(name="currency").first()
        cls.DOUBLE = FieldType.query.filter_by(name="double").first()
        cls.INTEGER = FieldType.query.filter_by(name="integer").first()
        cls.STRING = FieldType.query.filter_by(name="string").first()
        cls.TIME = FieldType.query.filter_by(name="time").first()


class ChartTypeConstants():
    """Constant ChartTypes used for easy type-checking in other modules"""
    try:
        LINE = ChartType.query.filter_by(name="line").first()
        BAR = ChartType.query.filter_by(name="bar").first()
        PIE = ChartType.query.filter_by(name="pie").first()
        TABLE_ONLY = ChartType.query.filter_by(name="table only").first()
    except:
        LINE = None
        BAR = None
        PIE = None
        TABLE_ONLY = None

    def __init__(self):
        """Initialize a ChartTypeConstants instance"""
        self.LINE = ChartType.query.filter_by(name="line").first()
        self.BAR = ChartType.query.filter_by(name="bar").first()
        self.PIE = ChartType.query.filter_by(name="pie").first()
        self.TABLE_ONLY = ChartType.query.filter_by(name="table only").first()

    @classmethod
    def reload(cls):
        """Reload the class constants"""
        cls.LINE = ChartType.query.filter_by(name="line").first()
        cls.BAR = ChartType.query.filter_by(name="bar").first()
        cls.PIE = ChartType.query.filter_by(name="pie").first()
        cls.TABLE_ONLY = ChartType.query.filter_by(name="table only").first()


class ChartDateTypeConstants():
    """Constant ChartTypes used for easy type-checking in other modules"""
    try:
        TODAY = ChartDateType.query.filter_by(name="today").first()
        FROM_WEEK = ChartDateType.query.filter_by(name="from_week").first()
        ROLLING_WEEK = ChartDateType.query.filter_by(name="rolling_week").first()
        FROM_MONTH = ChartDateType.query.filter_by(name="from_month").first()
        ROLLING_MONTH = ChartDateType.query.filter_by(name="rolling_month").first()
        FROM_YEAR = ChartDateType.query.filter_by(name="from_year").first()
        ROLLING_YEAR = ChartDateType.query.filter_by(name="rolling_year").first()
    except:
        TODAY = None
        FROM_WEEK = None
        ROLLING_WEEK = None
        FROM_MONTH = None
        ROLLING_MONTH = None
        FROM_YEAR = None
        ROLLING_YEAR = None

    def __init__(self):
        """Initialize a ChartDateTypeConstants instance"""
        self.TODAY = ChartDateType.query.filter_by(name="today").first()
        self.FROM_WEEK = ChartDateType.query.filter_by(name="from_week").first()
        self.ROLLING_WEEK = ChartDateType.query.filter_by(name="rolling_week").first()
        self.FROM_MONTH = ChartDateType.query.filter_by(name="from_month").first()
        self.ROLLING_MONTH = ChartDateType.query.filter_by(name="rolling_month").first()
        self.FROM_YEAR = ChartDateType.query.filter_by(name="from_year").first()
        self.ROLLING_YEAR = ChartDateType.query.filter_by(name="rolling_year").first()

    @classmethod
    def reload(cls):
        """Reload the class constants"""
        cls.TODAY = ChartDateType.query.filter_by(name="today").first()
        cls.FROM_WEEK = ChartDateType.query.filter_by(name="from_week").first()
        cls.ROLLING_WEEK = ChartDateType.query.filter_by(name="rolling_week").first()
        cls.FROM_MONTH = ChartDateType.query.filter_by(name="from_month").first()
        cls.ROLLING_MONTH = ChartDateType.query.filter_by(name="rolling_month").first()
        cls.FROM_YEAR = ChartDateType.query.filter_by(name="from_year").first()
        cls.ROLLING_YEAR = ChartDateType.query.filter_by(name="rolling_year").first()


class FieldDataDummy():
    """Class to hold dummy data for a Field when a value is missing"""
    def __init__(self, ds):
        """Initialize the FieldDataDummy"""
        self.ds = ds
        self.value = 'null'

    def __repr__(self):
        """Return a representation of this FieldDataDummy"""
        return '<FieldDataDummy for {ds}>'.format(ds=self.ds)

    @property
    def pretty_value(self):
        """Return an empty string, this is needed since we call .pretty_value elsewhere"""
        return ''
