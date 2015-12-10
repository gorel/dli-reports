"""Models for the admin module

Author: Logan Gore
This file is responsible for defining models that belong in the admin module.
"""

import datetime
import os

from dli_app import db
from dli_app import mail

from flask_mail import Message


class ErrorReport(db.Model):
    """Class representing bug reports and feature requests"""
    id = db.Column(db.Integer, primary_key=True)
    is_bug = db.Column(db.Boolean)
    error_text = db.Column(db.Text)
    user_text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sent = db.Column(db.Boolean)
    time = db.Column(db.DateTime)

    def __init__(self, is_bug, error_text, user_text, user):
        """Initialize the ErrorReport model"""
        self.is_bug = is_bug
        self.error_text = error_text
        self.user_text = user_text
        self.user = user
        self.sent = False
        self.time = datetime.datetime.now()

    @property
    def email_format(self):
        """Format the ErrorReport neatly for emailing purposes"""
        this_type = 'Bug Report' if self.is_bug else 'Feature Request'
        error_text = ''
        if self.error_text:
            error_text = 'Error: {text}'.format(text=self.error_text)
        return "{id}. {type} sent by {user} at {time}\n{user_text}\n{error_text}\n".format(
            id=self.id,
            type=this_type,
            user=self.user.name,
            time=self.time.strftime('%I:%M%p on %Y-%m-%d'),
            user_text=self.user_text,
            error_text=error_text,
        )

    def __repr__(self):
        """Return a human-readable representation of this ErrorReport"""
        this_type = 'Bug Report' if self.is_bug else 'Feature Request'
        return '<ErrorReport #{id} ({type})>'.format(id=self.id, type=this_type)

    @classmethod
    def send_new(cls):
        """Send new ErrorReports to the project developers"""
        error_reports = cls.query.filter_by(sent=False).all()
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        title = 'Bug Reports and Feature Requests {}'.format(today)
        msg = Message(title, recipients=[os.environ['DLI_REPORTS_DEV_EMAIL']])
        if error_reports:
            msg.body = '\n\n'.join(er.email_format for er in error_reports)
        else:
            msg.body = 'No Bug Reports or Feature Requests were submitted today.'
        mail.send(msg)
        for er in error_reports:
            er.sent = True
        db.session.commit()
