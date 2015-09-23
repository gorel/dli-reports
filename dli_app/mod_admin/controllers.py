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

# Import main DB and Login Mangaer for app
from dli_app import db, login_manager

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
    Report,
)

# Create a blueprint for this module
mod_admin = Blueprint('admin', __name__, url_prefix='/admin')

# Set all routing for the module
@mod_admin.route('/home', methods=['GET'])
@login_required
def home():
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
    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    form = AddLocationForm(request.form)
    if form.validate_on_submit():
        # TODO
        pass
    else:
        return render_template('admin/edit_locations.html', form=form)

@mod_admin.route('/edit_locations/delete/<loc_id>/', methods=['POST'])
@login_required
def delete_location(loc_id):
    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    if loc_id.isdigit():
        db.session.delete(Location.get(int(loc_id)))
        db.session.commit()
        flash(
            "Location deleted successfully.",
            "alert-success",
        )

    return redirect(url_for('admin.edit_locations'))


@mod_admin.route('/edit_departments/', methods=['GET', 'POST'])
@login_required
def edit_departments():
    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    form = AddDepartmentForm(request.form)
    if form.validate_on_submit():
        # TODO
        pass
    else:
        return render_template('admin/edit_departments.html', form=form)

@mod_admin.route('/edit_departments/delete/<dep_id>/', methods=['POST'])
@login_required
def delete_department(dep_id):
    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    if dep_id.isdigit():
        db.session.delete(Department.get(int(dep_id)))
        db.session.commit()
        flash(
            "Department deleted successfully.",
            "alert-success",
        )

    return redirect(url_for('admin.edit_departments'))

@mod_admin.route('/edit_fields/', methods=['GET', 'POST'])
@login_required
def edit_fields():
    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    form = AddFieldForm(request.form)
    if form.validate_on_submit():
        # TODO
        pass
    else:
        return render_template('admin/edit_fields.html', form=form)

@mod_admin.route('/edit_fields/delete/<field_id>/', methods=['POST'])
@login_required
def delete_field(field_id):
    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    if field_id.isdigit():
        db.session.delete(Field.get(int(field_id)))
        db.session.commit()
        flash(
            "Field deleted successfully.",
            "alert-success",
        )

    return redirect(url_for('admin.edit_fields'))

@mod_admin.route('/edit_users/', methods=['GET', 'POST'])
@login_required
def edit_users():
    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    form = AddUserForm(request.form)
    if form.validate_on_submit():
        subject = "Invitation to DLI Reports"
        body = None
        # TODO: Send user a registration link to the email
    else:
        return render_template('admin/edit_users.html', form=form)

@mod_admin.route('/edit_users/delete/<user_id>/', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash(
            "Sorry! You don't have permission to access that page.",
            "alert-warning",
        )
        return redirect(url_for('default.home'))

    if user_id.isdigit():
        db.session.delete(Field.get(int(user_id)))
        db.session.commit()
        flash(
            "User deleted successfully.",
            "alert-success",
        )

    return redirect(url_for('admin.edit_users'))
