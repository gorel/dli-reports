"""Extremely simple schedule task to send new ErrorReports daily.

Author: Logan Gore
This file will schedule a daily task to send an email to the developers
of the new bug reports and feature requests. It's important to remember
to send the mail from the context of the app. Otherwise an exception will
be thrown.
"""

import json
import os
import requests
import schedule
import time

from dli_app import app
from dli_app.mod_admin.models import ErrorReport

URL = os.environ['DLI_REPORTS_GITHUB_ISSUES_URL']
USERNAME = os.environ['DLI_REPORTS_GITHUB_USERNAME']
PASSWORD = os.environ['DLI_REPORTS_GITHUB_PASSWORD']
AUTH = (USERNAME, PASSWORD)

def job():
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

# Schedule the job and run forever
schedule.every().day.at("21:59").do(job)
while True:
    schedule.run_pending()
    time.sleep(60)
