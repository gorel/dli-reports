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

# Import main DB and Login Manager for app
from dli_app import db, login_manager

# Import forms
#from dli_app.mod_wiki.forms import (
#)

# Import models
#from dli_app.mod_wiki.models import (
#)

# Create a blueprint for this module
mod_wiki = Blueprint('wiki', __name__, url_prefix='/wiki')

# Set all routing for the module
@mod_wiki.route('/', methods=['GET'])
def home():
    return render_template('wiki/home.html')

@mod_wiki.route('/<page_name>', methods=['GET', 'POST'])
def view_page(page_name):
    return render_template('wiki/view.html')