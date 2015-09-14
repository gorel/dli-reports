from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from werkzeug import (
    check_password_hash,
    generate_password_hash
)

# Import main DB for app
from dli_app import db

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
def home():
    pass
