"""Controller for the account module

Author: Logan Gore
This file is responsible for loading all site pages under /account.
"""

from flask import (
    Blueprint,
    render_template,
)

from flask_login import (
    login_required,
)

# Create a blueprint for this module
mod_account = Blueprint('account', __name__, url_prefix='/account')


# Set all routing for the module
@mod_account.route('/home', methods=['GET'])
@login_required
def home():
    """Render the account home page"""
    return render_template('account/home.html')
