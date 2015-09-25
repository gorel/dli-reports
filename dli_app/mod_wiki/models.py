"""Models for the wiki module

Author: Logan Gore
This file is responsible for defining models that belong in the wiki module.
"""

from dli_app import db


class WikiPage(db.Model):
    """Model for a page on the wiki"""
    __tablename__ = 'wiki_page'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    content = db.Column(db.Text)
    # TODO: Add other necessary columns and bookkeeping information

    def __init__(self):
        """Initiialize a WikiPage model"""
        pass

    def __repr__(self):
        """Return a descriptive representation of a WikiPage"""
        return '<WikiPage %r>' % self.name
