"""Tasks the site should run in the background on a schedule

Author: Logan Gore

Tasks:
1. ErrorReport email sending
Send an email to the developers of the new bug reports and feature requests daily.

2. Invalid expired PasswordResets
PasswordResets that have reached their expiration date should be deleted.
"""

import datetime
import json
import os
import requests
import schedule
import time

from dli_app import app
from dli_app.mod_admin.models import ErrorReport
from dli_app.mod_auth.models import PasswordReset


URL = os.environ['DLI_REPORTS_GITHUB_ISSUES_URL']
USERNAME = os.environ['DLI_REPORTS_GITHUB_USERNAME']
PASSWORD = os.environ['DLI_REPORTS_GITHUB_PASSWORD']
AUTH = (USERNAME, PASSWORD)


def email_error_reports():
    """Send an email to the developers of the new bug reports and feature requests daily."""
    # First create Github issues for each report
    for er in ErrorReport.query.filter_by(sent=False):
        bug_or_enhancement = 'enhancement'
        if er.is_bug:
            bug_or_enhancement = 'bug'

        params = json.dumps({
            'title': er.user_text,
            'body': er.email_format,
            'milestone': 1,
            'labels': [bug_or_enhancement],
        })
        requests.post(URL, auth=AUTH, data=params)

    # Next, send all issues in one email report to the developers
    with app.app_context():
        ErrorReport.send_new()


def delete_expired_pw_resets():
    """PasswordResets that have reached their expiration date should be deleted."""
    now = datetime.datetime.now()
    for pw_reset in PasswordReset.query.filter(PasswordReset.expiration < now):
        db.session.delete(pw_reset)
    db.session.commit()


# Schedule the jobs and run forever
schedule.every().day.at("21:59").do(email_error_reports)
schedule.every().day.at("23:59").do(delete_expired_pw_resets)


# Run all scheduled jobs forever
while True:
    schedule.run_pending()
    time.sleep(60)
