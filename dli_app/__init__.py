"""Base module for the DLI Reports app.

Author: Logan Gore
This module creates the app and initializes all startup code.
"""

# System imports
import sys

# Flask imports
from flask import (
    Flask,
    flash,
    render_template,
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
)

# Define the web app
sys.stdout.write('Creating Flask app...')
app = Flask(__name__)
sys.stdout.write('Done\n')

# Configurations for the app
sys.stdout.write('Loading config from object...')
app.config.from_object('config')
sys.stdout.write('Done\n')

# Define the database
sys.stdout.write('Defining SQLAlchemy database...')
db = SQLAlchemy(app)
sys.stdout.write('Done\n')

# Create the login manager
sys.stdout.write('Creating login manager...')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "/auth/login"
sys.stdout.write('Done\n')

# Register error handlers
sys.stdout.write('Registering error handlers...')
@app.errorhandler(404)
def not_found(error):
    """Render the default 404 template"""
    return render_template('404.html', error=error), 404
sys.stdout.write('Done\n')

# Define form error handler
sys.stdout.write('Creating form error handler...')
def flash_form_errors(form):
    """Flash form errors to the user"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                "%s: %s" % (getattr(form, field).label.text, error),
                "alert-danger",
            )
sys.stdout.write('Done\n')

# Import all blueprints from controllers
from dli_app.controllers import mod_default
from dli_app.mod_account.controllers import mod_account
from dli_app.mod_admin.controllers import mod_admin
from dli_app.mod_auth.controllers import mod_auth
from dli_app.mod_reports.controllers import mod_reports
from dli_app.mod_wiki.controllers import mod_wiki

# Register blueprints
sys.stdout.write('Registering blueprint modules...')
app.register_blueprint(mod_default)
app.register_blueprint(mod_account)
app.register_blueprint(mod_admin)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_reports)
app.register_blueprint(mod_wiki)
sys.stdout.write('Done\n')

sys.stdout.write('\nApp done loading.\n')
