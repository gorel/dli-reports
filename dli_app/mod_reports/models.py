from dli_app import db

class Report(db.Model):
    __tablename__ = "report"
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        # TODO: Find a way of describing this report
        return '<Report>'

class Field(db.Model):
    __tablename__ = "field"
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        # TODO: Find a way of describing this field
        return '<Field>'
