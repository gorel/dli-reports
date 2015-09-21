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
from dli_app import db, login_manager

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
    # TODO: Only allow registration from an approved email link
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        # TODO: Lots of error checking for unique values

        location = Location.get(form.location.data)
        if location is None:
            flash('Invalid location.', 'alert-warning')
            # TODO: Keep everything else populated somehow
            return redirect(url_for('auth.register'))

        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
            location=location,
        )
        db.session.add(user)

        db.session.commit()

        # Log the user in and redirect to the homepage
        login_user(user)
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
        user = User.get_by_email(form.email.data)

        if user is None:
            flash('No account with that email exists!', 'alert-warning')
            return redirect(url_for('auth.login'))

        if not user.check_password(form.password.data):
            flash('Incorrect password! Try again?', 'alert-warning')
            # TODO: Prepopulate email field somehow
            return redirect(url_for('auth.login'))

        # User has authenticated. Log in.
        login_user(user, remember=form.remember.data)
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
