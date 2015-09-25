"""Controller for the wiki module

Author: Logan Gore
This file is responsible for loading all site pages under /wiki.
"""

from flask import (
    Blueprint,
    render_template,
)

from dli_app.mod_wiki.models import (
    WikiPage,
)

# Create a blueprint for this module
mod_wiki = Blueprint('wiki', __name__, url_prefix='/wiki')


# Set all routing for the module
@mod_wiki.route('/', methods=['GET'])
def home():
    """Render the wiki homepage"""
    return render_template('wiki/home.html')


@mod_wiki.route('/<page_name>', methods=['GET', 'POST'])
def view_page(page_name):
    """ Render a specific page of the wiki"""
    page = WikiPage.query.filter_by(name=page_name).first()
    if page is None:
        return render_template('wiki/404.html'), 404

    return render_template('wiki/view.html', page=page)
