"""Controller for the auth module

Author: Logan Gore
This file is responsible for loading all site pages under /auth.
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
    login_user,
    logout_user,
)

# Import forms
from dli_app.mod_auth.forms import (
    LoginForm,
    RegistrationForm,
    ForgotForm,
)

# Import models
from dli_app.mod_auth.models import (
    Location,
)

from dli_app import (
    db,
    flash_form_errors,
)

# Create a blueprint for this module
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


# Set all routing for the module
@mod_auth.route('/register/<registration_key>/', methods=['GET', 'POST'])
def register(registration_key):
    """Register a new user

    If the user successfully submitted the form, add the new user to the db,
    commit the session, and login the user before redirecting to the home page.
    Otherwise, render the template to show the user the registration page.
    Arguments:
    registration_key - the unique key for registering the user's account
    """

    form = RegistrationForm()
    if form.validate_on_submit():
        db.session.add(form.user)
        db.session.commit()

        # Log the user in and redirect to the homepage
        login_user(form.user, form.remember.data)
        flash("You have created a new account at DLI-Reports", "alert-success")
        return redirect(request.args.get('next') or url_for('default.home'))
    else:
        form.registration_key.data = registration_key
        form.location.choices = [
            (location.id, location.name) for location in Location.query.all()
        ]

        flash_form_errors(form)
        return render_template('auth/register.html', form=form)


@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():
    """Login the user

    If the user successfully submitted the form, log them in. Otherwise,
    render the login form for the user to input their information.
    """

    form = LoginForm()
    if form.validate_on_submit():
        # User has authenticated. Log in.
        login_user(form.user, remember=form.remember.data)
        flash("You are now logged into DLI-Reports", "alert-success")
        return redirect(request.args.get('next') or url_for('default.home'))
    else:
        flash_form_errors(form)
        return render_template('auth/login.html', form=form)


@mod_auth.route('/logout/', methods=['POST'])
def logout():
    """Log the user out of their account

    As long as the current user is authenticated, log them out of thier
    account then redirect to the site index. Don't set login required,
    because it will send the user to the login page before redirecting them
    to logout. It doesn't make much sense to the user.
    """

    if current_user.is_authenticated:
        logout_user()
    flash('You have successfully logged out.', 'alert-success')
    return redirect(url_for('default.home'))

@mod_auth.route('/resetpass/', methods=['GET', 'POST'])
def resetpass():
    """Reset the user's password

    If the user successfully submitted the form, send a password 
    reset email. Otherwise, render the reset form again.
    """

    form = ForgotForm()
    if form.validate_on_submit():
        # Email is authenticated and sent
        email = form.email.data
	#Create User Specific URL here
        pw_reset = PasswordReset(
            user_id= User.get_by_email(self.email.data),
            key=''.join(
                random.choice(
                    string.ascii_letters + string.digits
                ) for _ in range(60)
            ),
        )
        db.session.add(pw_reset)
        db.session.commit()
        #ADD EMAIL STUFF HERE
	mail=Mail()
	title='Reset your Password'
	content='Click this link to reset your password'
	sender='cs490testing@gmail.com'
	msg=Message(title,sender=sender,recipients=[email])
	msg.body=content
	mail.send(msg)
        flash("Email sent!", "alert-success")
        return redirect(url_for('default.home'))
    else:
        flash_form_errors(form)
    	return render_template('auth/resetpass.html', form=form)

