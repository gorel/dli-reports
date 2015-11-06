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
    send_file,
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
    Chart,
    ChartType,
    ChartDateType,
    Report,
)

# Import forms
from dli_app.mod_reports.forms import (
    ChangeDateForm,
    ChangeDateAndDepartmentForm,
    CreateChartForm,
    EditChartForm,
    CreateReportForm,
    SubmitReportDataForm,
    EditReportForm,
    SearchForm,
)

# Create a blueprint for this module
mod_reports = Blueprint('reports', __name__, url_prefix='/reports')


# Set all routing for the module
@mod_reports.route('/me', methods=['GET'])
@mod_reports.route('/me/', methods=['GET'])
@mod_reports.route('/me/<int:page_num>', methods=['GET'])
@login_required
def my_reports(page_num=1):
    """Show the user all of their reports"""
    # Download reports that belong to the current user
    reports = Report.query.filter_by(
        user_id=current_user.id,
    ).paginate(page_num)
    form = SearchForm()
    return render_template('reports/me.html', reports=reports, form=form)

@mod_reports.route('/all', methods=['GET'])
@mod_reports.route('/all/', methods=['GET'])
@mod_reports.route('/all/<int:page_num>', methods=['GET'])
@login_required
def all_reports(page_num=1):
    """Show the user all reports (made by anyone"""
    reports = Report.query.paginate(page_num)
    form = SearchForm()
    return render_template('reports/all.html', reports=reports, form=form)


@mod_reports.route('/favorite/<int:report_id>', methods=['POST'])
@mod_reports.route('/favorite/<int:report_id>/', methods=['POST'])
@login_required
def favorite_report(report_id):
    """Add a report to the user's favorite reports"""
    report = Report.query.get(report_id)
    if report is None:
        flash(
            "No report with that report_id found!",
            "alert-warning",
        )
    else:
        current_user.favorite(report)
        db.session.commit()
        flash(
            "Added Report: {name} to favorites list".format(name=report.name),
            "alert-success",
        )
    return redirect(request.args.get('next') or url_for('reports.my_reports'))


@mod_reports.route('/unfavorite/<int:report_id>', methods=['POST'])
@mod_reports.route('/unfavorite/<int:report_id>/', methods=['POST'])
@login_required
def unfavorite_report(report_id):
    """Remove a report from the user's favorite reports"""
    report = Report.query.get(report_id)
    if report is None:
        flash(
            "No report with that report_id found!",
            "alert-warning",
        )
    else:
        current_user.unfavorite(report)
        db.session.commit()
        flash(
            "Removed Report: {name} from favorites list".format(
                name=report.name,
            ),
            "alert-success",
        )
    return redirect(request.args.get('next') or url_for('reports.my_reports'))


@mod_reports.route('/create', methods=['GET', 'POST'])
@mod_reports.route('/create/', methods=['GET', 'POST'])
@login_required
def create_report():
    """Create a new report

    If the user successfully submitted the form, add the new report to the db,
    commit the session, and redirect the user to the list of their reports.
    Otherwise, render the template to show the user the create report page.
    """

    LocalCreateReportForm = CreateReportForm.get_instance()
    for department in Department.query.all():
        LocalCreateReportForm.add_department(department)

    form = LocalCreateReportForm()
    form.user_id.data = current_user.id
    if form.validate_on_submit():
        # Add the new report to the database
        db.session.add(form.report)
        db.session.commit()

        return redirect(url_for('reports.my_reports'))
    else:
        flash_form_errors(form)
        return render_template('reports/create.html', form=form)


@mod_reports.route('/<int:report_id>/data', methods=['GET', 'POST'])
@mod_reports.route('/<int:report_id>/data/', methods=['GET', 'POST'])
@mod_reports.route('/<int:report_id>/data/<ds>/<int:dept_id>', methods=['GET', 'POST'])
@login_required
def submit_report_data(report_id, ds=datetime.now().strftime('%Y-%m-%d'), dept_id=None):
    """Submit new report data

    If the user successfully submitted the form, submit all of the report
    data, commit the session, and redirect the user to view their reports.
    Otherwise, render the template to show the user the report data submission
    form.
    """

    # Check to see if the user picked a different day or department
    change_form = ChangeDateAndDepartmentForm()
    if change_form.validate_on_submit() and change_form.department.data:
        return redirect(
            url_for(
                'reports.submit_report_data',
                report_id=report_id,
                ds=change_form.ds,
                dept_id=change_form.dept_id,
            )
        )

    report = Report.query.get(report_id)

    # We must generate the dynamic form before loading it
    if dept_id is None:
        dept_id = current_user.department.id

    department = Department.query.get(dept_id)
    if department is None:
        flash(
            "No department with that ID found.",
            "alert-warning",
        )
        return redirect(url_for('reports.submit_report_data', report_id=report_id))

    LocalSubmitReportDataForm = SubmitReportDataForm.get_instance()

    for field in report.fields:
        if field.department_id == dept_id:
            LocalSubmitReportDataForm.add_field(field)

    # *Now* the form is properly initialized
    form = LocalSubmitReportDataForm()
    if form.validate_on_submit() and form.ds.data:
        # Delete any old values that already existed
        for stale_value in form.stale_values:
            db.session.delete(stale_value)

        # Also "invalidate" any existing Excel sheets that used this data
        for data_point in form.data_points:
            for report in data_point.field.reports:
                if report.excel_file_exists(ds):
                    report.remove_excel_file(ds)

        # Add all of the new data points
        db.session.add_all(form.data_points)
        db.session.commit()

        flash(
            "Report data successfully submitted.",
            "alert-success",
        )
        return redirect(url_for('reports.my_reports'))
    else:
        flash_form_errors(change_form)
        flash_form_errors(form)
        form.ds.data = ds

        # Set the change_form defaults
        change_form.date.data = datetime.strptime(ds, "%Y-%m-%d")
        change_form.department.data = dept_id or current_user.department.id

        for field in form.instance_fields:
            # This line allows us to dynamically load the field data
            formfield = getattr(form, field.name)
            if formfield.data is None:
                existing_value = field.data_points.filter_by(ds=ds).first()
                if existing_value is not None:
                    formfield.data = existing_value.value

        chunk_size = 10
        field_list = form.instance_fields
        chunked_fields = [field_list[n:n+chunk_size] for n in range(0, len(field_list), chunk_size)]

        return render_template(
            'reports/submit_data.html',
            change_form=change_form,
            form=form,
            chunked_fields=chunked_fields,
            report=report,
            department=department,
            ds=ds,
        )


@mod_reports.route('/view/<int:report_id>', methods=['GET', 'POST'])
@mod_reports.route('/view/<int:report_id>/', methods=['GET', 'POST'])
@mod_reports.route('/view/<int:report_id>/<ds>/', methods=['GET', 'POST'])
@login_required
def view_report(report_id, ds=datetime.now().strftime('%Y-%m-%d')):
    """Show the user a specific report"""

    form = ChangeDateForm()
    if form.validate_on_submit():
        return redirect(
            url_for('reports.view_report', report_id=report_id, ds=form.ds)
        )

    report = Report.query.get(report_id)
    if report is None:
        flash(
            "Report not found!",
            "alert-warning",
        )
        return redirect(url_for('reports.my_reports'))

    dept_data = report.collect_dept_data_for_template(ds)
    return render_template(
        'reports/view.html',
        form=form,
        report=report,
        dept_data=dept_data,
        ds=ds,
    )

@mod_reports.route('/download/<int:report_id>/<ds>', methods=['GET'])
@mod_reports.route('/download/<int:report_id>/<ds>/', methods=['GET'])
@login_required
def download_report(report_id, ds):
    """Download a report as an Excel file"""
    report = Report.query.get(report_id)
    if report is None:
        flash(
            "Report not found!",
            "alert-warning",
        )
    else:
        if not report.excel_file_exists(ds):
            report.create_excel_file(ds)
        return send_file(
            report.excel_filepath_for_ds(ds),
            as_attachment=True,
        )


@mod_reports.route('/delete/<int:report_id>', methods=['POST'])
@mod_reports.route('/delete/<int:report_id>/', methods=['POST'])
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
        # Before deleting the report, check to see if any other users have
        # favorited this report. If so, simply transfer ownership to them
        current_user.unfavorite(report)
        if report.favorite_users:
            user = report.favorite_users[0]
            report.user = user
            db.session.commit()
            flash(
                "Report ownership was transferred to {{ user.name }} since "
                "the report was in that user's favorites list.",
                "alert-success",
            )
        else:
            db.session.delete(report)
            db.session.commit()
            flash(
                "Report deleted",
                "alert-success",
            )
    return redirect(request.args.get('next') or url_for('reports.my_reports'))


@mod_reports.route('/edit/<int:report_id>', methods=['GET','POST'])
@mod_reports.route('/edit/<int:report_id>/', methods=['GET','POST'])
@login_required
def edit_report(report_id):
    """Edit the specified report"""
    report = Report.query.get(report_id)
    if report is None:
        flash(
            "Report not found!",
            "alert-warning",
        )
    elif not current_user.is_admin and not report.user.id == current_user.id:
        flash(
            "You don't have permission to edit that.",
            "alert-warning",
        )
    else:
        LocalEditReportForm = EditReportForm.get_instance()
        for department in Department.query.all():
            LocalEditReportForm.add_department(department)

        form = LocalEditReportForm()
        if form.validate_on_submit():
            flash('Report: {name} has been updated'.format(name=form.report.name), 'alert-success')
            db.session.commit()

            return redirect(url_for('reports.my_reports'))
        else:
            flash_form_errors(form)
            form.name.data = report.name
            form.report_id.data = report_id
            for department in Department.query.all():
                set_fields = [field for field in report.fields if field.department.id == department.id]
                getattr(form, department.name).data = [f.id for f in set_fields]
            return render_template('reports/edit.html', form=form, report=report)


@mod_reports.route('/search', methods=['GET', 'POST'])
@mod_reports.route('/search/', methods=['GET', 'POST'])
@login_required
def search():
    """Search for reports that contains a keyword in owner,name,tag,department,location"""
    form = SearchForm()
    if form.validate_on_submit():
        return render_template('reports/search_results.html', reports=form.reports)
    else:
        flash_form_errors(form)
        return render_template('reports/search.html', form=form)


@mod_reports.route('/charts', methods=['GET'])
@mod_reports.route('/charts/', methods=['GET'])
@mod_reports.route('/charts/me', methods=['GET'])
@mod_reports.route('/charts/me/', methods=['GET'])
@mod_reports.route('/charts/me/<int:page_num>', methods=['GET'])
@mod_reports.route('/charts/me/<int:page_num>/', methods=['GET'])
@login_required
def my_charts(page_num=1):
    """View the current user's charts"""
    # Download charts that belong to the current user
    charts = Chart.query.filter_by(owner_id=current_user.id).paginate(page_num)
    return render_template('reports/my_charts.html', charts=charts)


@mod_reports.route('/charts/all', methods=['GET'])
@mod_reports.route('/charts/all/', methods=['GET'])
@mod_reports.route('/charts/all/<int:page_num>', methods=['GET'])
@mod_reports.route('/charts/all/<int:page_num>/', methods=['GET'])
@login_required
def all_charts(page_num=1):
    """View all charts"""
    # Download all charts in the database
    charts = Chart.query.paginate(page_num)
    return render_template('reports/all_charts.html', charts=charts)


@mod_reports.route('/charts/view/<int:chart_id>', methods=['GET'])
@mod_reports.route('/charts/view/<int:chart_id>/', methods=['GET'])
@login_required
def view_chart(chart_id):
    """View a specific chart"""
    chart = Chart.query.get(chart_id)
    if chart is None:
        flash('Error: Chart not found', 'alert-warning')
        return redirect(url_for('reports.my_charts'))
    else:
        return render_template('reports/view_chart.html', chart=chart)


@mod_reports.route('/charts/favorite/<int:chart_id>', methods=['POST'])
@mod_reports.route('/charts/favorite/<int:chart_id>/', methods=['POST'])
@login_required
def favorite_chart(chart_id):
    """Add a chart to the user's favorite charts"""
    chart = Chart.query.get(chart_id)
    if chart is None:
        flash(
            "No chart with that chart_id found!",
            "alert-warning",
        )
    else:
        current_user.favorite_chart(chart)
        db.session.commit()
        flash(
            "Added Chart: {name} to favorites list".format(name=chart.name),
            "alert-success",
        )
    return redirect(request.args.get('next') or url_for('reports.my_charts'))


@mod_reports.route('/charts/unfavorite/<int:chart_id>', methods=['POST'])
@mod_reports.route('/charts/unfavorite/<int:chart_id>/', methods=['POST'])
@login_required
def unfavorite_chart(chart_id):
    """Remove a chart from the user's favorite charts"""
    chart = Chart.query.get(chart_id)
    if chart is None:
        flash(
            "No chart with that chart_id found!",
            "alert-warning",
        )
    else:
        current_user.unfavorite_chart(chart)
        db.session.commit()
        flash(
            "Removed Chart: {name} from favorites list".format(name=chart.name),
            "alert-success",
        )
    return redirect(request.args.get('next') or url_for('reports.my_charts'))


@mod_reports.route('/charts/create', methods=['GET', 'POST'])
@mod_reports.route('/charts/create/', methods=['GET', 'POST'])
@login_required
def create_chart():
    """Create a new chart

    If the user successfully submitted the form, add the new chart to the db,
    commit the session, and redirect the user to the list of their charts.
    Otherwise, render the template to show the user the create chart page.
    """

    LocalCreateChartForm = CreateChartForm.get_instance()
    for department in Department.query.all():
        LocalCreateChartForm.add_department(department)

    form = LocalCreateChartForm()
    form.user_id.data = current_user.id
    form.chart_type.choices = [
        (ctype.id, ctype.name.upper()) for ctype in ChartType.query.all()
    ]
    form.chart_date_type.choices = [
        (cdtype.id, cdtype.pretty_value) for cdtype in ChartDateType.query.all()
    ]
    if form.validate_on_submit():
        # Add the new chart to the database
        db.session.add(form.chart)
        db.session.commit()

        return redirect(url_for('reports.my_charts'))
    else:
        flash_form_errors(form)
        return render_template('reports/create_chart.html', form=form)


@mod_reports.route('charts/delete/<int:chart_id>', methods=['POST'])
@mod_reports.route('charts/delete/<int:chart_id>/', methods=['POST'])
@login_required
def delete_chart(chart_id):
    """Delete the specified chart"""
    chart = Chart.query.get(chart_id)
    if chart is None:
        flash("Error: Chart not found!", "alert-warning")
    elif not current_user.is_admin and not chart.user.id == current_user.id:
        flash(
            "You don't have permission to delete that.",
            "alert-warning",
        )
    else:
        # Before deleting the chart, check to see if any other users have
        # favorited this chart. If so, simply transfer ownership to them
        current_user.unfavorite_chart(chart)
        if chart.favorite_users:
            user = chart.favorite_users[0]
            chart.user = user
            db.session.commit()
            flash(
                "Chart ownership was transferred to {{ user.name }} since "
                "the chart was in that user's favorites list.",
                "alert-success",
            )
        else:
            db.session.delete(chart)
            db.session.commit()
            flash("Chart deleted", "alert-success")
    return redirect(request.args.get('next') or url_for('reports.my_charts'))


@mod_reports.route('/charts/edit/<int:chart_id>', methods=['GET','POST'])
@mod_reports.route('/charts/edit/<int:chart_id>/', methods=['GET','POST'])
@login_required
def edit_chart(chart_id):
    """Edit the specified chart"""
    chart = Chart.query.get(chart_id)
    if chart is None:
        flash(
            "Error: Chart not found!",
            "alert-warning",
        )
    elif not current_user.is_admin and not chart.user.id == current_user.id:
        flash(
            "You don't have permission to delete that.",
            "alert-warning",
        )
    else:
        LocalEditChartForm = EditChartForm.get_instance()
        for department in Department.query.all():
            LocalEditChartForm.add_department(department)

        form = LocalEditChartForm()
        form.chart_type.choices = [
            (ctype.id, ctype.name.upper()) for ctype in ChartType.query.all()
        ]
        form.chart_date_type.choices = [
            (cdtype.id, cdtype.name.upper().replace('_', ' ')) for cdtype in ChartDateType.query.all()
        ]
        if form.validate_on_submit():
            flash('Chart: {name} has been updated'.format(name=form.chart.name), 'alert-success')
            db.session.commit()

            return redirect(url_for('reports.my_charts'))
        else:
            flash_form_errors(form)
            form.chart_id.data = chart_id
            form.name.data = chart.name
            form.chart_type.data = chart.ctype.id
            form.chart_date_type.data = chart.cdtype.id
            form.with_table.data = chart.with_table
            for department in Department.query.all():
                set_fields = [field for field in chart.fields if field.department.id == department.id]
                getattr(form, department.name).data = [f.id for f in set_fields]
            return render_template('reports/edit_chart.html', form=form, chart=chart)

