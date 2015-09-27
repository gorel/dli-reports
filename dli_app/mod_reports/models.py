"""Models for the reports module

Author: Logan Gore
This file is responsible for defining models that belong in the reports module.
"""

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
    user_id = db.Column(db.Integer, index=True)
    rep_name = db.Column(db.String(64))
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

    def __init__(self):
        """Initialize a Report model"""
        self.filename = EXCEL_FILE_DIR + self.name + ""
        pass

    def generate_filename(self, ds):
        return "{directory}/{filename}-{ds}".format(
            directory=EXCEL_FILE_DIR,
            filename=self.name,
            ds=ds,
        )

    def __repr__(self):
        """Return a descriptive representation of a Report"""
        return '<Report %r>' % self.rep_name

    def to_excel(self, ds):
        filename = self.generate_filename(ds)
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        # TODO: For field in report:
            # field_data = { dept: [(Field, FieldData), ] }
        # Write all of the data to the worksheet
        workbook.close()

    def delete_excel_file(self, ds):
        filename = self.generate_filename(ds)
        os.remove(filename)


class Field(db.Model):
    """Model for a Field within a Report"""
    __tablename__ = "field"
    id = db.Column(db.Integer, primary_key=True)
    field_type = db.relationship('FieldType')
	department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
	name = db.Column(db.String(32))

    def __init__(self):
        """Initialize a Field model"""
        pass

    def __repr__(self):
        """Return a descriptive representation of a Field"""
        return '<Field %r>' %r name


class FieldType(db.Model):
    """Model for the type of a Field"""
    __tablename__ = "field_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)

    def __init__(self):
        """Initialize a FieldType model"""
        pass

    def __repr__(self):
        """Return a descriptive representation of a FieldType"""
        return '<Field Type %r>' % self.name


class FieldData(db.Model):
    """Model for the actual data stored in a Field"""
    __tablename__ = "field_data"
    id = db.Column(db.Integer, primary_key=True)
	date_stamp = db.Column(db.DateTime, primary_key=True)
	field_id = db.Column(db.Integer, db.ForeignKey("field.id"))
	ivalue = db.Column(db.BigInteger)
	dvalue = db.Column(db.Double)
	svalue = db.Column(db.String(128))

    def __init__(self):
        """Initialize a FieldData model"""
        pass

    def __repr__(self):
        """Return a descriptive representation of a FieldData"""
        return '<FieldData %r>' % svalue


class Tag(db.Model):
    """Model for a Tag associated with a Report"""
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)

    def __init__(self):
        """Initialize a Tag model"""
        pass

    def __repr__(self):
        """Return a descriptive representation of a Tag"""
        return '<Tag %r>' % self.name
