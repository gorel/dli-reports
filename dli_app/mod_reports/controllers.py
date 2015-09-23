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
)

# Import main DB and Login Manager for app
from dli_app import db, login_manager

# Import forms
from dli_app.mod_reports.forms import (
    CreateReportForm,
    SubmitReportDataForm,
)

# Create a blueprint for this module
mod_reports = Blueprint('reports', __name__, url_prefix='/reports')

# Set all routing for the module
@mod_reports.route('/me', methods=['GET'])
@login_required
def my_reports():
    # TODO: Download reports that belong to the current user
    reports = None
    return render_template('reports/me.html', reports=reports)

@mod_reports.route('/all', methods=['GET'])
@login_required
def all_reports():
    reports = Report.query.all()
    return render_template('reports/all.html', reports=reports)

@mod_reports.route('/create', methods=['GET', 'POST'])
@login_required
def create_report():
    form = CreateReportForm(request.form)
    if form.validate_on_submit():
        # TODO
        pass
    else:
        return render_template('reports/create.html', form=form)

@mod_reports.route('/data', methods=['GET', 'POST'])
@login_required
def submit_report_data():
    form = SubmitReportDataForm(request.form)
    if form.validate_on_submit():
        # TODO
        pass
    else:
        return render_template('reports/data.html', form=form)

@mod_reports.route('/view/<report_id>', methods=['GET'])
@login_required
def view_report(report_id):
    return render_template('reports/view.html')
