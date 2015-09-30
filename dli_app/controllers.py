"""Default routing for the app not within any module

Author: Logan Gore
This file is only responsible for loading the site index page.
"""

from flask import (
    Blueprint,
    render_template,
)


# Create a blueprint for this module
mod_default = Blueprint('default', __name__)


# Set all routing for the default app (not within modules)
@mod_default.route('/')
@mod_default.route('/home')
@mod_default.route('/index.html')
def home():
    """Render the site index page"""
    return render_template('index.html')
