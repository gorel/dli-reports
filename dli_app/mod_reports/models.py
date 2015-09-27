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
    user_id = db.Column(db.Integer, index=True)
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

    def __repr__(self):
        return '<Report %r>' % self.name

class Field(db.Model):
    __tablename__ = "field"
    id = db.Column(db.Integer, primary_key=True)
    field_type = db.relationship('FieldType')
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))
    name = db.Column(db.String(32))
    def __repr__(self):
        return '<Field %r>' %r self.name

class FieldType(db.Model):
    __tablename__ = "field_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    data_points = db.relationship(
    'FieldData',
    backref='field',
    )
    def __repr__(self):
        return '<Field Type %r>' % self.name

class FieldData(db.Model):
    __tablename__ = "field_data"
    id = db.Column(db.Integer, primary_key=True)
    date_stamp = db.Column(db.DateTime, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey("field.id"))
    ivalue = db.Column(db.BigInteger)
    dvalue = db.Column(db.Double)
    svalue = db.Column(db.String(128))
    def __repr__(self):
        return '<FieldData %r>' % self.svalue

class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Tag %r>' % self.name
