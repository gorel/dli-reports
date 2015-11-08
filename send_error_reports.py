"""Extremely simple schedule task to send new ErrorReports daily.

Author: Logan Gore
This file will schedule a daily task to send an email to the developers
of the new bug reports and feature requests. It's important to remember
to send the mail from the context of the app. Otherwise an exception will
be thrown.
"""

import schedule
import time

from dli_app import app
from dli_app.mod_admin.models import ErrorReport

def job():
    with app.app_context():
        ErrorReport.send_new()

# Schedule the job and run forever
schedule.every().day.at("21:59").do(job)
while True:
    schedule.run_pending()
    time.sleep(60)
