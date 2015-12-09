"""Base module for the DLI Reports app.

Author: Logan Gore
This module creates the app and initializes all startup code.
"""

# System imports
import os
import sys

# Flask imports
from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect

# Other imports
from htmlmin.main import minify


ENVIRON_KEYS = [
    'DLI_REPORTS_ADMIN_PASSWORD',
    'DLI_REPORTS_SITE_URL',
    'DLI_REPORTS_DEV_EMAIL',
]

# Check for environment variables.  Exit if they are not set properly
for key in ENVIRON_KEYS:
    if not key in os.environ:
        sys.stderr.write('Error! Environment variables not set up properly.\n')
        sys.stderr.write('Missing variable: {}\n'.format(key))
        sys.exit()

# Define the web app
sys.stdout.write('Creating Flask app...')
sys.stdout.flush()
app = Flask(__name__)
sys.stdout.write('Done\n')

# Configurations for the app
sys.stdout.write('Loading config from object...')
sys.stdout.flush()
app.config.from_object('config')
sys.stdout.write('Done\n')

# Define the database
sys.stdout.write('Defining SQLAlchemy database...')
sys.stdout.flush()
db = SQLAlchemy(app)
sys.stdout.write('Done\n')

# Create the login manager
sys.stdout.write('Creating login manager...')
sys.stdout.flush()
login_manager = LoginManager(app)
login_manager.login_view = "/auth/login"
sys.stdout.write('Done\n')

# Configure Flask-Mail
sys.stdout.write('Configuring Mail Server...')
sys.stdout.flush()
mail = Mail(app)
sys.stdout.write('Done\n')

# Enable CSRF protection
sys.stdout.write('Enabling CSRF protection...')
sys.stdout.flush()
csrf = CsrfProtect(app)
sys.stdout.write('Done\n')

# Register error handlers
sys.stdout.write('Registering error handlers...')
sys.stdout.flush()
@app.errorhandler(404)
def not_found(error):
    """Render the default 404 template"""
    return render_template('404.html', error=error), 404
@app.errorhandler(500)
def server_error(error):
    """Redirect to the bugsplat page"""
    return redirect(url_for('admin.bugsplat', error=error))
sys.stdout.write('Done\n')

# Minify sent HTML strings
sys.stdout.write('Loading HTML minifier...')
@app.after_request
def response_minify(response):
    """Minify HTML response to decrease bandwidth"""
    if response.content_type == u'text/html; charset=utf-8':
        response.set_data(minify(response.get_data(as_text=True)))
    return response
sys.stdout.write('Done\n')

# Define form error handler
sys.stdout.write('Creating form error handler...')
sys.stdout.flush()
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
sys.stdout.write('Importing blueprints from controllers...')
sys.stdout.flush()
from dli_app.controllers import mod_default
from dli_app.mod_account.controllers import mod_account
from dli_app.mod_admin.controllers import mod_admin
from dli_app.mod_auth.controllers import mod_auth
from dli_app.mod_reports.controllers import mod_reports
from dli_app.mod_wiki.controllers import mod_wiki
sys.stdout.write('Done\n')

# Register blueprints
sys.stdout.write('Registering blueprint modules...')
sys.stdout.flush()
app.register_blueprint(mod_default)
app.register_blueprint(mod_account)
app.register_blueprint(mod_admin)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_reports)
app.register_blueprint(mod_wiki)
sys.stdout.write('Done\n')

sys.stdout.write('\nApp done loading.\n')
