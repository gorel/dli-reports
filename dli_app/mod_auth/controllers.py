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
#from dli_app.mod_auth.forms import (
#)

# Import models
#from dli_app.mod_auth.models import (
#)

# Create a blueprint for this module
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set all routing for the module
@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():
    pass

@mod_auth.route('/logout/', methods=['POST'])
def logout():
    pass
