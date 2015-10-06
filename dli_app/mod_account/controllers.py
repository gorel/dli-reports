"""Controller for the account module

Author: Logan Gore
This file is responsible for loading all site pages under /account.
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

from dli_app import (
    db,
    flash_form_errors,
)

from dli_app.mod_auth.models import (
    Department,
    Location,
)

from dli_app.mod_account.forms import (
    EditAccountForm,
)

# Create a blueprint for this module
mod_account = Blueprint('account', __name__, url_prefix='/account')


# Set all routing for the module
@mod_account.route('/home/', methods=['GET'])
@login_required
def home():
    """Render the account home page"""
    return render_template('account/home.html')


@mod_account.route('/edit/', methods=['GET', 'POST'])
@login_required
def edit():
    """Edit the user's account settings"""
    form = EditAccountForm()
    form.user_id.data = current_user.id

    # Dynamically load the location and department choices
    form.location.choices = [
        (location.id, location.name) for location in Location.query.all()
    ]

    form.department.choices = [
        (dept.id, dept.name) for dept in Department.query.all()
    ]

    if form.validate_on_submit():
        db.session.commit()
        flash(
            "Your account has been updated successfully",
            "alert-success",
        )
        return redirect(request.args.get('next') or url_for('account.home'))
    else:
        flash_form_errors(form)

        # Set the form defaults
        form.name.data = current_user.name
        form.location.default = current_user.location.id
        form.department.default = current_user.department.id

        return render_template('account/edit.html', form=form)
