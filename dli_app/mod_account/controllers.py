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

# Import main DB and Login Manager for app
from dli_app import db, login_manager

# Import forms
#from dli_app.mod_account.forms import (
#)

# Import models
#from dli_app.mod_account.models import (
#)

# Create a blueprint for this module
mod_account = Blueprint('account', __name__, url_prefix='/account')

# Set all routing for the module
@mod_account.route('/home', methods=['GET'])
@login_required
def home():
    return render_template('account/home.html')
