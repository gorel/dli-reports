"""Models for the wiki module

Author: Logan Gore
This file is responsible for defining models that belong in the wiki module.
"""

import datetime

from dli_app import db

from flask_login import (
    current_user,
)

class WikiPage(db.Model):
    """Model for a page on the wiki"""
    __tablename__ = 'wiki_page'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    content = db.Column(db.Text)
    modtime = db.Column(db.String(32))
    editor = db.Column(db.String(64))
    views = db.Column(db.Integer, index=True)

    def __init__(self, name, content):
        """Initiialize a WikiPage model"""
        self.name = name
        self.content = content
        self.modtime = datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')
        self.editor = current_user.name
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
