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
#from dli_app.mod_admin.forms import (
#)

# Import models
#from dli_app.mod_admin.models import (
#)

# Create a blueprint for this module
mod_admin = Blueprint('admin', __name__, url_prefix='/admin')

# Set all routing for the module
@mod_admin.route('/home', methods=['GET'])
@login_required
def home():
    # TODO: Check if user is an administrator
    return render_template('admin/home.html')
