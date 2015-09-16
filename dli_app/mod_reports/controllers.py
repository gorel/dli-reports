from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from flask.ext.login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

# Import main DB and Login Manager for app
from dli_app import db, login_manager

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
@login_required
def my_reports():
    return render_template('reports/me.html')

@mod_reports.route('/all', methods=['GET'])
@login_required
def all_reports():
    return render_template('reports/all.html')

@mod_reports.route('/create', methods=['GET', 'POST'])
@login_required
def create_report():
    if request.method == 'GET':
        return render_template('reports/create.html')
    else:
        # TODO: Submit new report creation
        pass

@mod_reports.route('/data', methods=['GET', 'POST'])
@login_required
def submit_report_data():
    if request.method == 'GET':
        return render_template('reports/data.html')
    else:
        # TODO: Submit new report data
        pass

@mod_reports.route('/view/<report_id>', methods=['GET'])
@login_required
def view_report(report_id):
    return render_template('reports/view.html')
