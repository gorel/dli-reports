"""Controller for the reports module

Author: Logan Gore
This file is responsible for loading all site pages under /reports.
"""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from flask_login import (
    current_user,
    login_required,
)

# Import main db for app
from dli_app import db

# Import models
from dli_app.mod_reports.models import (
    Report,
)

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
    """Show the user all of their reports"""
    # Download reports that belong to the current user
    reports = Report.query.filter_by(user_id=current_user.id).all()
    return render_template('reports/me.html', reports=reports)


@mod_reports.route('/all', methods=['GET'])
@login_required
def all_reports():
    """Show the user all reports (made by anyone"""
    reports = Report.query.all()
    return render_template('reports/all.html', reports=reports)


@mod_reports.route('/create', methods=['GET', 'POST'])
@login_required
def create_report():
    """Create a new report

    If the user successfully submitted the form, add the new report to the db,
    commit the session, and redirect the user to the list of their reports.
    Otherwise, render the template to show the user the create report page.
    """

    form = CreateReportForm(request.form)
    if form.validate_on_submit():
        # Add the new report to the database
        db.session.add(form.report)
        db.session.commit()

        return redirect(url_for('reports.my_reports'))
    else:
        return render_template('reports/create.html', form=form)


@mod_reports.route('/data', methods=['GET', 'POST'])
@login_required
def submit_report_data():
    """Submit new report data

    If the user successfully submitted the form, submit all of the report
    data, commit the session, and redirect the user to view their reports.
    Otherwise, render the template to show the user the report data submission
    form.
    """

    form = SubmitReportDataForm(request.form)
    if form.validate_on_submit():
        # TODO: Submit all of the form data

        flash(
            "Report data successfully submitted.",
            "alert-success",
        )
        return redirect(url_for('reports.my_reports'))
    else:
        return render_template('reports/data.html', form=form)


@mod_reports.route('/view/<int:report_id>', methods=['GET'])
@login_required
def view_report(report_id):
    """Show the user a specific report"""
    report = Report.get(report_id)
    if report is None:
        flash(
            "Report not found!",
            "alert-warning",
        )
        return redirect(url_for('reports.my_reports'))

    return render_template('reports/view.html', report=report)
