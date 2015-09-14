from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from werkzeug import (
    check_password_hash,
    generate_password_hash
)

# Import main DB for app
from dli_app import db

# Import forms
#from dli_app.mod_reports.forms import (
#)

# Import models
#from dli_app.mod_reports.models import (
#)

# Create a blueprint for this module
mod_reports = Blueprint('reports', __name__, url_prefix='/reports')

# Set all routing for the module
@mod_reports.route('/me', methods=['GET'])
def my_reports():
    pass

@mod_reports.route('/all', methods=['GET'])
def all_reports():
    pass

@mod_reports.route('/create', methods=['GET', 'POST'])
def create_report():
    pass

@mod_reports.route('/data', methods=['GET', 'POST'])
def submit_report_data():
    pass

@mod_reports.route('/view/<report_id>', methods=['GET'])
def view_report(report_id):
    pass
