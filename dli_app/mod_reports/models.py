"""Models for the reports module

Author: Logan Gore
This file is responsible for defining models that belong in the reports module.
"""

from dli_app import db


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
    # TODO: Fill out remaining fields
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
        pass

    def __repr__(self):
        """Return a descriptive representation of a Report"""
        # TODO: Find a way of describing this report
        return '<Report>'


class Field(db.Model):
    """Model for a Field within a Report"""
    __tablename__ = "field"
    id = db.Column(db.Integer, primary_key=True)
    field_type = db.relationship('FieldType')
    # TODO: Fill out remaining fields

    def __init__(self):
        """Initialize a Field model"""
        pass

    def __repr__(self):
        """Return a descriptive representation of a Field"""
        # TODO: Find a way of describing this field
        return '<Field>'


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
    # TODO: Fill out remaining fields

    def __init__(self):
        """Initialize a FieldData model"""
        pass

    def __repr__(self):
        """Return a descriptive representation of a FieldData"""
        # TODO: Find a way of describing this field data
        return '<FieldData>'


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
