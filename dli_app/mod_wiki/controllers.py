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
#from dli_app.mod_wiki.forms import (
#)

# Import models
#from dli_app.mod_wiki.models import (
#)

# Create a blueprint for this module
mod_wiki = Blueprint('wiki', __name__, url_prefix='/wiki')

# Set all routing for the module
@mod_wiki.route('/home', methods=['GET'])
def home():
    pass
