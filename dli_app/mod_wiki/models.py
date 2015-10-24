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
    views = db.Column(db.Integer, index=True)
    # TODO: Add other necessary columns and bookkeeping information

    def __init__(self, name, content):
        """Initiialize a WikiPage model"""
        self.name = name
        self.content = content
        self.views = 0

    def __repr__(self):
        """Return a descriptive representation of a WikiPage"""
        return '<WikiPage %r>' % self.name

    def with_toc(self):
        """Return the page contents with a Table of Contents header"""
        full_text = """
        [TOC]

        {content}
        """.format(content=self.content)
        return full_text
