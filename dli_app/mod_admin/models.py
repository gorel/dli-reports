"""Models for the admin module

Author: Logan Gore
This file is responsible for defining models that belong in the admin module.
"""

import datetime
import os

from dli_app import (
    db,
    mail,
)

from flask_mail import (
    Message,
)

class ErrorReport(db.Model):
    """Class representing bug reports and feature requests"""
    id = db.Column(db.Integer, primary_key=True)
    is_bug = db.Column(db.Boolean)
    error_text = db.Column(db.Text)
    user_text = db.Column(db.Text)
    sent = db.Column(db.Boolean)

    def __init__(self, is_bug, error_text, user_text):
        """Initialize the ErrorReport model"""
        self.is_bug = is_bug
        self.error_text = error_text
        self.user_text = user_text
        self.sent = False

    @classmethod
    def send_new(cls):
        error_reports = cls.query.filter_by(sent=False).all()
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        title = 'Bug Reports and Feature Requests {}'.format(today)
        msg = Message(title, recipients=[os.environ['DLI_REPORTS_DEV_EMAIL']])
        msg.body = '\n\n'.join(er.user_text for er in error_reports)
        mail.send(msg)
        for er in error_reports:
            er.sent = True
        db.session.commit()
