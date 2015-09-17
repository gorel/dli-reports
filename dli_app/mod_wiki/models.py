from dli_app import db

class WikiPage(db.Model):
    __tablename__ = 'wiki_page'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    content = db.Column(db.Text)
    # TODO: Add other necessary columns and bookkeeping information

    def __init__(self):
        pass

    def __repr__(self):
        return '<WikiPage %r>' % name
