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

# Import main DB for app
from dli_app import db, login_manager

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
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        # Login code here
        return redirect('/')

@mod_auth.route('/logout/', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))
