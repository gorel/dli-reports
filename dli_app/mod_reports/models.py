"""Models for the reports module

Author: Logan Gore
This file is responsible for defining models that belong in the reports module.
"""

import collections
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


class Report(db.Model):
    """Model for a DLI Report"""
    __tablename__ = "report"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    name = db.Column(db.String(64))
    fields = db.relationship(
        'Field',
        secondary=report_fields,
        backref='reports',
    )
    tags = db.relationship(
        'Tag',
        secondary=report_tags,
        backref='reports',
    )

    def __init__(self, user_id, name, fields, tags):
        """Initialize a Report model"""
        self.user_id = user_id
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


class Field(db.Model):
    """Model for a Field within a Report"""
    __tablename__ = "field"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    ftype_id = db.Column(db.Integer, db.ForeignKey("field_type.id"))
    ftype = db.relationship("FieldType")
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    data_points = db.relationship(
        'FieldData',
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
                data_point = "No data submitted."
        return data_point


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
            return "ERROR: Type %s not supported!" % ftype

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
            return "ERROR: Type %s not supported!" % ftype


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

    @classmethod
    def reload(cls):
        """Reload the class constants"""
        cls.CURRENCY = FieldType.query.filter_by(name="currency").first()
        cls.DOUBLE = FieldType.query.filter_by(name="double").first()
        cls.INTEGER = FieldType.query.filter_by(name="integer").first()
        cls.STRING = FieldType.query.filter_by(name="string").first()
        cls.TIME = FieldType.query.filter_by(name="time").first()
