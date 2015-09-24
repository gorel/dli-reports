from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)

from flask.ext.login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from werkzeug import (
    check_password_hash,
    generate_password_hash,
)

# Import main DB and Login Manager for app
from dli_app import login_manager

# Import forms
from dli_app.mod_auth.forms import (
    LoginForm,
    RegistrationForm,
)

# Import models
from dli_app.mod_auth.models import (
    Location,
    User,
)

# Create a blueprint for this module
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set all routing for the module
@mod_auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        db.session.add(self.user)
        db.session.commit()

        # Log the user in and redirect to the homepage
        login_user(form.user, form.remember.data)
        return redirect(request.args.get('next') or url_for('default.home'))
    else:
        form.location.choices = [
            (location.id, location.name) for location in Location.query.all()
        ]
        return render_template('auth/register.html', form=form)

@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        # User has authenticated. Log in.
        login_user(form.user, remember=form.remember.data)
        return redirect(request.args.get('next') or url_for('default.home'))
    else:
        return render_template('auth/login.html', form=form)

@mod_auth.route('/logout/', methods=['POST'])
def logout():
    # Don't set login required, because it will send the user to the login page
    # before redirecting them to logout. It doesn't make much sense to the user.
    if current_user.is_authenticated:
        logout_user()
    flash('You have successfully logged out.', 'alert-success')
    return redirect(url_for('/'))
