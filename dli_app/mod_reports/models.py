"""Models for the reports module

Author: Logan Gore
This file is responsible for defining models that belong in the reports module.
"""

import collections
import datetime
import glob
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


def generate_date_list(start, end, step=None):
    """Generate a ds list along an interval"""
    if not step:
        step = 1
        if (end - start).days > 100:
            step = 7
        elif (end - start).days > 20:
            step = 3
    delta = datetime.timedelta(days=step)
    dates = []

    while start < end:
        dates.append(start)
        start += delta
    dates.append(end)
    return dates


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
    ds = db.Column(db.String(16), index=True)
    field_id = db.Column(db.Integer, db.ForeignKey("field.id"))
    ivalue = db.Column(db.BigInteger)
    dvalue = db.Column(db.Float)
    svalue = db.Column(db.String(128))

    def __init__(self, ds, field, value):
        """Initialize a FieldData model"""
        FieldTypeConstants.reload()
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
            if ':' in value:
                parts = value.split(':')
            elif '.' in value:
                # Some people use '.' to denote minutes/seconds
                parts = value.split('.')
            else:
                # If no : or ., assume the value listed is seconds
                parts = ['0', value]

            # If the user listed something like ':00', make sure we can still parse
            parts = [x or '0' for x in parts]
            self.ivalue = int(parts[0]) * 60
            if len(parts) == 2:
                self.ivalue += int(parts[1])

    def __repr__(self):
        """Return a descriptive representation of a FieldData"""
        return '<FieldData of %r>' % self.field.name

    @property
    def value(self):
        """Property to easily retrieve the FieldData's value"""
        FieldTypeConstants.reload()
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
        FieldTypeConstants.reload()
        ftype = self.field.ftype
        if ftype == FieldTypeConstants.CURRENCY:
            dollars = self.ivalue / 100
            cents = self.ivalue % 100
            return "${dollars}.{cents:02d}".format(
                dollars=dollars,
                cents=cents,
            )
        elif ftype == FieldTypeConstants.DOUBLE:
            return self.dvalue
        elif ftype == FieldTypeConstants.INTEGER:
            return self.ivalue
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

    def generate_filename(self, start_ds, end_ds):
        """Generate the filename for the Excel sheet for downloads"""
        return "{filename}-{start}-to-{end}.xlsx".format(
            filename=self.name,
            start=start_ds,
            end=end_ds,
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

    def excel_filepath_for_ds(self, start_ds, end_ds):
        """Return the absolute filepath for the Excel sheet on the given ds"""
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            EXCEL_FILE_DIR,
            self.generate_filename(start_ds, end_ds),
        )

    def excel_file_exists(self, start_ds, end_ds):
        """Determine whether or not an Excel file for this ds exists"""
        return os.path.exists(self.excel_filepath_for_ds(start_ds, end_ds))

    def create_excel_file(self, start_ds, end_ds):
        """Generate an Excel sheet with this Report's data

        Arguments:
        start_ds - Date stamp for the start day of Report data to generate
        end_ds - Date stamp for the end day of Report data to generate
        """

        excel_helper = ExcelSheetHelper(
            filepath=self.excel_filepath_for_ds(start_ds, end_ds),
            report=self,
            date_list=generate_date_list(
                datetime.datetime.strptime(start_ds, '%Y-%m-%d'),
                datetime.datetime.strptime(end_ds, '%Y-%m-%d'),
                step=1,
            ),
        )
        excel_helper.write_all(self.collect_dept_fields(start_ds, end_ds))
        excel_helper.finalize()

    def remove_excel_files(self):
        """Delete the Excel files for this Report"""
        basepath = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            EXCEL_FILE_DIR,
        )
        globpath = os.path.join(basepath, self.name + '*.xlsx')

        for filename in glob.glob(globpath):
            os.remove(os.path.join(basepath, filename))

    def collect_dept_fields(self, start_ds, end_ds):
        """Collect all of the department data for this Report

        The best way we can do this is to create a complex dict:
        {dept : {field : {ds : value}}}

        Arguments:
        start_ds - the beginning ds for data to collect
        end_ds - the ending ds for data to collect
        """
        dept_data = {}
        for field in self.fields:
            field_data = {
                pt.ds: pt.value
                for pt in field.data_points.filter(FieldData.ds >= start_ds).filter(FieldData.ds <= end_ds)
            }
            if not dept_data.get(field.department.name):
                dept_data[field.department.name] = {}
            dept_data[field.department.name][field] = field_data
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


class Chart(db.Model):
    """Model for a DLI Chart"""
    __tablename__ = "chart"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    with_table = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    ctype_id = db.Column(db.Integer, db.ForeignKey("chart_type.id"))
    ctype = db.relationship(ChartType, backref="charts")
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

    def __init__(self, name, with_table, user, ctype, fields, tags):
        """Initialize a Chart model"""
        self.name = name
        self.with_table = with_table
        self.user = user
        self.ctype = ctype
        self.fields = fields
        self.tags = tags

    def __repr__(self):
        """Return a descriptive representation of a Chart"""
        return '<Chart %r>' % self.name

    @property
    def is_pie_chart(self):
        ChartTypeConstants.reload()
        return self.ctype == ChartTypeConstants.PIE

    def data_points(self, min_date, max_date=None, ds_format=False):
        """Retrieve the data points needed for this chart"""
        if ds_format:
            min_ds = min_date
            max_ds = max_date
        else:
            min_ds = min_date.strftime('%Y-%m-%d')
            max_ds = datetime.datetime.now().strftime('%Y-%m-%d')
            if max_date:
                max_ds = max_date.strftime('%Y-%m-%d')

        return {
            field.identifier: {
                str(fdata.ds): str(fdata.value)
                for fdata in field.data_points.filter(FieldData.ds >= min_ds).filter(FieldData.ds <= max_ds)
            }
            for field in self.fields
        }

    @property
    def tagnames(self):
        """Helper function to get the names of the Report's tags"""
        return [tag.name for tag in self.tags]

    def generated_js(self):
        """Property that represents this chart generated as C3 JavaScript"""
        min_date = datetime.datetime.now()
        ChartTypeConstants.reload()
        if self.ctype != ChartTypeConstants.PIE:
            min_date = min_date - datetime.timedelta(days=14)

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
        now = datetime.datetime.now()
        days = (now - min_date).days + 1
        ds_list = [min_date + datetime.timedelta(days=x) for x in range(0, days)]
        return sorted([x.strftime('%Y-%m-%d') for x in ds_list])


class ExcelSheetHelper():
    """Helper class to write data to an Excel Sheet for DLI Reports

    Provides functions that write all Report data to an Excel file.
    Overloads the write method to write data while keeping track of the sheet's
    row and column information.
    """

    def __init__(self, filepath, report, date_list):
        """Initialize an ExcelSheetHelper by creating an XLSX Workbook"""
        self.report = report
        self.date_list = date_list

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
            "Report: {name}".format(name=self.report.name),
            self.report_name_format,
        )
        self.row += 1

        self.worksheet.write(
            self.row,
            self.col,
            "Data between {start} and {end}".format(
                start=self.date_list[0].strftime('%m/%d/%Y'),
                end=self.date_list[-1].strftime('%m/%d/%Y'),
            ),
            self.ds_format,
        )
        self.row += 1

        self.col += 1
        for date in self.date_list:
            # Write the ds headers
            self.worksheet.write(
                self.row,
                self.col,
                date.strftime('%m/%d/%Y'),
            )
            self.col += 1
        self.col = 0

    def write_all(self, dept_fields):
        """Write all of the data for a Report

        dept_fields is of the form:
        {dept : {field : {ds : value}}}
        """
        for dept in dept_fields.keys():
            self.write_dept_title(dept)
            for field in sorted(dept_fields[dept].keys(), key=lambda x: x.name):
                self.write_field(field, dept_fields[dept][field])

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

    def write_field(self, field, values):
        """Write a Field within a Report"""
        self.worksheet.write(
            self.row,
            self.col,
            field.name,
            self.field_format,
        )
        self.col += 1

        for date in self.date_list:
            # Write the data for each ds
            field_data = values.get(date.strftime('%Y-%m-%d'))
            if field_data:
                self.worksheet.write(
                    self.row,
                    self.col,
                    field_data,
                    self.get_format(field),
                )
            self.col += 1

        self.row += 1
        self.col = 0

    def get_format(self, field):
        """Get the format required for the specific field"""
        FieldTypeConstants.reload()
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
