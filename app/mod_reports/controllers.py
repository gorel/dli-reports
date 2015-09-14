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
from app import db

# Import forms
#from app.mod_reports.forms import (
#)

# Import models
#from app.mod_reports.models import (
#)

# Create a blueprint for this module
mod_reports = Blueprint('reports', __name__, url_prefix='/reports')

# Set all routing for the module
@mod_reports.route('/home', methods=['GET'])
def home():
    pass
