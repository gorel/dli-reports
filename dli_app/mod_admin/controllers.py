"""Controller for the admin module

Author: Logan Gore
This file is responsible for loading all site pages under /admin.
"""

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
    current_app,
)

from flask_mail import (
    Mail,
    Message,
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
    RegisterCandidate,
)

from dli_app.mod_reports.models import (
    Field,
    FieldType,
)

# Create a blueprint for this module
mod_admin = Blueprint('admin', __name__, url_prefix='/admin')


# Set all routing for the module
@mod_admin.route('/', methods=['GET'])
@mod_admin.route('/home', methods=['GET'])
@mod_admin.route('/home/', methods=['GET'])
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


@mod_admin.route('/edit_locations', methods=['GET', 'POST'])
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

    form = AddLocationForm()
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

        flash_form_errors(form)
        return render_template(
            'admin/edit_locations.html',
            form=form,
            locations=locations,
        )


@mod_admin.route('/edit_locations/delete/<int:loc_id>', methods=['POST'])
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

    location = Location.query.get(loc_id)
    if location is not None:
        db.session.delete(location)
        db.session.commit()

        flash(
            "Location deleted successfully.",
            "alert-success",
        )

    return redirect(url_for('admin.edit_locations'))



@mod_admin.route('/edit_departments', methods=['GET', 'POST'])
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

    form = AddDepartmentForm()
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

        flash_form_errors(form)
        return render_template(
            'admin/edit_departments.html',
            form=form,
            departments=departments,
        )


@mod_admin.route('/edit_departments/delete/<int:dept_id>', methods=['POST'])
@mod_admin.route('/edit_departments/delete/<int:dept_id>/', methods=['POST'])
@login_required
def delete_department(dept_id):
    """Delete a department

    First, perform a check that the user is an admin.
    Arguments:
    dept_id - The id of the department to be deleted, as defined in the db
    """

    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    department = Department.query.get(dept_id)
    if department is not None:
        db.session.delete(department)
        db.session.commit()

        flash(
            "Department deleted successfully.",
            "alert-success",
        )

    return redirect(url_for('admin.edit_departments'))


@mod_admin.route('/edit_fields', methods=['GET', 'POST'])
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

    form = AddFieldForm()

    # Dynamically load the department and type choices
    form.department.choices = [
        (dept.id, dept.name) for dept in Department.query.all()
    ]

    form.field_type.choices = [
        (ftype.id, ftype.name.upper()) for ftype in FieldType.query.all()
    ]

    if form.validate_on_submit():
        db.session.add(form.field)
        db.session.commit()

        flash(
            "Field added successfully",
            "alert-success",
        )
        return redirect(url_for('admin.edit_fields'))
    else:

        flash_form_errors(form)
        return render_template(
            'admin/edit_fields.html',
            form=form,
            departments=Department.query.all(),
        )


@mod_admin.route('/edit_fields/delete/<int:field_id>', methods=['POST'])
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

    field = Field.query.get(field_id)
    if field is not None:
        db.session.delete(field)
        db.session.commit()

        flash(
            "Field deleted successfully.",
            "alert-success",
        )

    return redirect(url_for('admin.edit_fields'))


@mod_admin.route('/edit_users', methods=['GET', 'POST'])
@mod_admin.route('/edit_users/', methods=['GET', 'POST'])
@mod_admin.route('/edit_users/<int:page_num>', methods=['GET', 'POST'])
@login_required
def edit_users(page_num=1):
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

    form = AddUserForm()
    if form.validate_on_submit():
        
        db.session.add(form.user)
        db.session.commit()
	candidate=RegisterCandidate.query.filter_by(email=form.user.email).first()
	if candidate is not None:
	    key = candidate.registration_key
	    mail = Mail(current_app)
	    title = 'Activate your account'
	    content = 'Please go to the link: '
	    url = '68.234.146.84:PORT/auth/register/'+key
	    sender = 'cs490testing@gmail.com'
	    recipient = candidate.email
	    msg = Message(title, sender=sender, recipients=[recipient])
	    msg.body = content + url
	    mail.send(msg)
            flash(
                "Sent an invite link to {email}".format(email=form.user.email),
                "alert-success",
            )
            return redirect(url_for('admin.edit_users'))
    else:
        # Get a list of users
        users = User.query.paginate(page_num)
        candidates = RegisterCandidate.query.all()

        flash_form_errors(form)
        return render_template(
            'admin/edit_users.html',
            form=form,
            users=users,
            candidates=candidates,
        )


@mod_admin.route('/edit_users/delete/<int:user_id>', methods=['POST'])
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

    if current_user.id == user_id:
        flash(
            "Now why would you try to delete your own account?",
            "alert-danger",
        )
        return redirect(url_for('admin.home'))

    user = User.query.get(user_id)
    if user is not None:
        for report in user.reports:
            current_user.unfavorite(report)
            if report.favorite_users:
                new_owner = report.favorite_users[0]
                report.user = new_owner
            else:
                db.session.delete(report)
        db.session.delete(user)
        db.session.commit()

        flash(
            "User deleted successfully.",
            "alert-success",
        )

    return redirect(url_for('admin.edit_users'))


@mod_admin.route('/edit_users/delete_candidate/<int:candidate_id>', methods=['POST'])
@mod_admin.route('/edit_users/delete_candidate/<int:candidate_id>/', methods=['POST'])
@login_required
def delete_candidate(candidate_id):
    """Delete a RegisterCandidate

    First, perform a check that the user is an admin.
    Arguments:
    candidate_id - The id of the candidate to be deleted, as defined in the db
    """

    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    candidate = RegisterCandidate.query.get(candidate_id)
    if candidate is not None:
        db.session.delete(candidate)
        db.session.commit()

        flash(
            "User deleted successfully.",
            "alert-success",
        )

    return redirect(url_for('admin.edit_users'))
