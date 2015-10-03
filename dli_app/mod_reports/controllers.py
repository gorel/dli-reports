"""Controller for the reports module

Author: Logan Gore
This file is responsible for loading all site pages under /reports.
"""

from datetime import datetime

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

# Import main db and form error handler for app
from dli_app import (
    db,
    flash_form_errors,
)

# Import models
from dli_app.mod_auth.models import (
    Department,
)

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
        flash_form_errors(form)
        return render_template('reports/create.html', form=form)


@mod_reports.route('/data/', methods=['GET', 'POST'])
@mod_reports.route('/data/<ds>/<int:dept_id>', methods=['GET', 'POST'])
@login_required
def submit_report_data(ds=datetime.now().strftime('%Y-%m-%d'), dept_id=None):
    """Submit new report data

    If the user successfully submitted the form, submit all of the report
    data, commit the session, and redirect the user to view their reports.
    Otherwise, render the template to show the user the report data submission
    form.
    """

    # We must generate the dynamic form before loading it
    if dept_id is None:
        dept_id = current_user.department.id

    department = Department.query.get(dept_id)
    if department is None:
        flash(
            "No department with that ID found.",
            "alert-warning",
        )
        return redirect(url_for('reports.submit_report_data'))

    LocalSubmitReportDataForm = SubmitReportDataForm.get_instance()

    for field in department.fields:
        LocalSubmitReportDataForm.add_field(field)

    # *Now* the form is properly initialized
    form = LocalSubmitReportDataForm()
    if form.validate_on_submit():
        # Delete any old values that already existed
        for stale_value in form.stale_values:
            db.session.delete(stale_value)

        # Add all of the new data points
        db.session.add_all(form.data_points)
        db.session.commit()

        flash(
            "Report data successfully submitted.",
            "alert-success",
        )
        return redirect(url_for('reports.my_reports'))
    else:
        flash_form_errors(form)
        form.ds.data = ds

        for field in form.instance_fields:
            # This line allows us to dynamically load the field data
            formfield = getattr(form, field.name)
            if formfield.data is None:
                existing_value = field.data_points.filter_by(ds=ds).first()
                if existing_value is not None:
                    formfield.data = existing_value

        return render_template(
            'reports/submit_data.html',
            form=form,
            department=department,
            ds=ds,
        )


@mod_reports.route('/view/<int:report_id>', methods=['GET'])
@login_required
def view_report(report_id):
    """Show the user a specific report"""
    report = Report.query.get(report_id)
    if report is None:
        flash(
            "Report not found!",
            "alert-warning",
        )
        return redirect(url_for('reports.my_reports'))

    return render_template('reports/view.html', report=report)


@mod_reports.route('/delete/<int:report_id>', methods=['POST'])
@login_required
def delete_report(report_id):
    """Delete the specified report"""
    report = Report.query.get(report_id)
    if report is None:
        flash(
            "Report not found!",
            "alert-warning",
        )
    elif not current_user.is_admin and not report.user.id == current_user.id:
        flash(
            "You don't have permission to delete that.",
            "alert-warning",
        )
    else:
        db.session.delete(report)
        flash(
            "Report deleted",
            "alert-success",
        )
    return redirect(url_for('reports.my_reports'))
