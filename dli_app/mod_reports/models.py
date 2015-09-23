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

    def __repr__(self):
        # TODO: Find a way of describing this report
        return '<Report>'

class Field(db.Model):
    __tablename__ = "field"
    id = db.Column(db.Integer, primary_key=True)
    field_type = db.relationship('FieldType')
    # TODO: Fill out remaining fields

    def __repr__(self):
        # TODO: Find a way of describing this field
        return '<Field>'

class FieldType(db.Model):
    __tablename__ = "field_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)

    def __repr__(self):
        return '<Field Type %r>' % self.name

class FieldData(db.Model):
    __tablename__ = "field_data"
    id = db.Column(db.Integer, primary_key=True)
    # TODO: Fill out remaining fields

    def __repr__(self):
        # TODO: Find a way of describing this field data
        return '<FieldData>'

class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Tag %r>' % self.name
