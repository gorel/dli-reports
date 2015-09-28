"""Controller for the admin module

Author: Logan Gore
This file is responsible for loading all site pages under /admin.
"""

import collections

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

# Import forms
from dli_app.mod_admin.forms import (
    AddDepartmentForm,
    AddFieldForm,
    AddLocationForm,
    AddUserForm,
)

# Import models
from dli_app.mod_auth.models import (
    Department,
    Location,
    User,
)

from dli_app.mod_reports.models import (
    Field,
)

# Create a blueprint for this module
mod_admin = Blueprint('admin', __name__, url_prefix='/admin')


# Set all routing for the module
@mod_admin.route('/home', methods=['GET'])
@login_required
def home():
    """Render the home page for administrative tasks

    If the user is not an admin, redirect to the site index and
    alert the user they don't have permission to view this page.
    """

    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    return render_template('admin/home.html')


@mod_admin.route('/edit_locations/', methods=['GET', 'POST'])
@login_required
def edit_locations():
    """Render the location editing page

    First perform a check to ensure the user is an admin.
    Load the "Add Location" form. If the user has submitted a new location,
    add it to the db and commit the session before redirecting the user to
    view the list of all locations. Otherwise, show the user the list of all
    locations.
    """

    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    form = AddLocationForm(request.form)
    if form.validate_on_submit():
        db.session.add(form.location)
        db.session.commit()

        flash(
            "Location added successfully",
            "alert-success",
        )
        return redirect(url_for('admin.edit_locations'))
    else:
        # Get a list of all locations
        locations = Location.query.all()
        return render_template(
            'admin/edit_locations.html',
            form=form,
            locations=locations,
        )


@mod_admin.route('/edit_locations/delete/<int:loc_id>/', methods=['POST'])
@login_required
def delete_location(loc_id):
    """Delete a location

    First, perform a check that the user is an admin.
    Arguments:
    loc_id - The id of the location to be deleted, as defined in the db
    """

    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    location = Location.get(int(loc_id))
    if location is not None:
        db.session.delete(location)
        db.session.commit()

        flash(
            "Location deleted successfully.",
            "alert-success",
        )

    return redirect(url_for('admin.edit_locations'))



@mod_admin.route('/edit_departments/', methods=['GET', 'POST'])
@login_required
def edit_departments():
    """Render the department editing page

    First perform a check to ensure the user is an admin.
    Load the "Add Department" form. If the user has submitted a new department,
    add it to the db and commit the session before redirecting the user to
    view the list of all departments. Otherwise, show the user the list of all
    departments.
    """

    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    form = AddDepartmentForm(request.form)
    if form.validate_on_submit():
        db.session.add(form.department)
        db.session.commit()

        flash(
            "Department added successfully",
            "alert-success",
        )
        return redirect(url_for('admin.edit_departments'))
    else:
        # Get a list of all departments
        departments = Department.query.all()
        return render_template(
            'admin/edit_departments.html',
            form=form,
            departments=departments,
        )


@mod_admin.route('/edit_departments/delete/<int:dep_id>/', methods=['POST'])
@login_required
def delete_department(dep_id):
    """Delete a department

    First, perform a check that the user is an admin.
    Arguments:
    dep_id - The id of the department to be deleted, as defined in the db
    """

    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    department = Department.get(int(dep_id))
    if department is not None:
        db.session.delete(department)
        db.session.commit()

        flash(
            "Department deleted successfully.",
            "alert-success",
        )

    return redirect(url_for('admin.edit_departments'))


@mod_admin.route('/edit_fields/', methods=['GET', 'POST'])
@login_required
def edit_fields():
    """Render the field editing page

    First perform a check to ensure the user is an admin.
    Load the "Add Field" form. If the user has submitted a new field,
    add it to the db and commit the session before redirecting the user to
    view the list of all fields. Otherwise, show the user the list of all
    fields.
    """

    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    form = AddFieldForm(request.form)
    if form.validate_on_submit():
        db.session.add(form.field)
        db.session.commit()

        flash(
            "Field added successfully",
            "alert-success",
        )
        return redirect(url_for('admin.edit_fields'))
    else:
        # Get a list of all fields and return a dict of the form:
        # {dept: [field1, field2, ...]} for easy templating
        dept_fields = collections.defaultdict(list)
        for field in Field.query.all():
            dept_fields[field.department].append(field)
        return render_template(
            'admin/edit_fields.html',
            form=form,
            dept_fields=dept_fields,
        )


@mod_admin.route('/edit_fields/delete/<int:field_id>/', methods=['POST'])
@login_required
def delete_field(field_id):
    """Delete a field from a department

    First, perform a check that the user is an admin.
    Arguments:
    field_id - The id of the field to be deleted, as defined in the db
    """

    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    field = Field.get(int(field_id))
    if field is not None:
        db.session.delete(field)
        db.session.commit()

        flash(
            "Field deleted successfully.",
            "alert-success",
        )

    return redirect(url_for('admin.edit_fields'))


@mod_admin.route('/edit_users/', methods=['GET', 'POST'])
@login_required
def edit_users():
    """Render the user editing page

    First perform a check to ensure the user is an admin.
    Load the "Add User" form. If the user has submitted a new user,
    add it to the db and commit the session before redirecting the user to
    view the list of all users. Otherwise, show the user the list of all
    users.
    """

    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    form = AddUserForm(request.form)
    if form.validate_on_submit():
        # TODO: Send user a registration link to the email
        return redirect(url_for('admin.edit_users'))
    else:
        # Get a list of users
        users = User.query.all()
        return render_template(
            'admin/edit_users.html',
            form=form,
            users=users,
        )


@mod_admin.route('/edit_users/delete/<int:user_id>/', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete a user

    First, perform a check that the user is an admin.
    Arguments:
    user_id - The id of the user to be deleted, as defined in the db
    """

    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    user = User.get(user_id)
    if user is not None:
        db.session.delete(user)
        # TODO: Delete/move the user's reports, too
        db.session.commit()

        flash(
            "User deleted successfully.",
            "alert-success",
        )

    return redirect(url_for('admin.edit_users'))
