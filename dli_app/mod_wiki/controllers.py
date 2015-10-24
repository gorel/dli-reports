"""Controller for the wiki module

Author: Logan Gore
This file is responsible for loading all site pages under /wiki.
"""

from markdown import (
    Markdown,
)

from markdown.extensions import (
    extra,
    nl2br,
    toc,
    wikilinks,
)

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for,
)

from flask_login import (
    login_required,
)

from dli_app import (
    db,
    flash_form_errors,
)

from dli_app.mod_wiki.models import (
    WikiPage,
)

from dli_app.mod_wiki.forms import (
    EditWikiPageForm,
    SearchForm,
)

EXTENSIONS = [
    extra.ExtraExtension(),
    nl2br.Nl2BrExtension(),
    toc.TocExtension(),
    wikilinks.WikiLinkExtension(base_url='/wiki/'),
]

MD = Markdown(extensions=EXTENSIONS)

# Create a blueprint for this module
mod_wiki = Blueprint('wiki', __name__, url_prefix='/wiki')


# Set all routing for the module
@mod_wiki.route('/', methods=['GET'])
@mod_wiki.route('/home', methods=['GET'])
@mod_wiki.route('/home/', methods=['GET'])
def home():
    """Render the wiki homepage"""
    page = WikiPage.query.filter_by(name='home').first()
    html = ''

    if page is not None:
        html = MD.convert(page.content)

    form = SearchForm()
    return render_template('wiki/home.html', form=form, html=html)


@mod_wiki.route('/<page_name>', methods=['GET'])
@mod_wiki.route('/<page_name>/', methods=['GET'])
def view_page(page_name):
    """ Render a specific page of the wiki"""
    page = WikiPage.query.filter_by(name=page_name).first()
    if page is None:
        return render_template('wiki/404.html'), 404

    html = MD.convert(page.content)
    return render_template('wiki/view.html', page=page, html=html, toc=MD.toc)


@mod_wiki.route('/edit', methods=['GET', 'POST'])
@mod_wiki.route('/edit/', methods=['GET', 'POST'])
@mod_wiki.route('/edit/<page_name>/', methods=['GET', 'POST'])
@login_required
def edit_page(page_name=''):
    """Edit a specific page of the wiki"""
    page = WikiPage.query.filter_by(name=page_name).first()

    form = EditWikiPageForm()
    if form.validate_on_submit():
        page = WikiPage.query.filter_by(name=form.name.data).first()

        # Update the WikiPage's information
        if page is not None:
            page.name = form.page.name
            page.content = form.page.content
            # TODO: Additional fields that need to be set here
            flash(
                "WikiPage updated successfully",
                "alert-success",
            )
        # Create a new WikiPage
        else:
            db.session.add(form.page)
            flash(
                "WikiPage added successfully",
                "alert-success",
            )

        db.session.commit()
        return redirect(url_for('wiki.view_page', page_name=form.page.name))
    else:
        flash_form_errors(form)
        if page is not None:
            form.name.data = page.name
            form.content.data = page.content
        return render_template('wiki/edit.html', form=form)


@mod_wiki.route('/delete/<int:page_id>', methods=['POST'])
@mod_wiki.route('/delete/<int:page_id>/', methods=['POST'])
@login_required
def delete_page(page_id):
    """Delete a given WikiPage"""
    page = WikiPage.query.get(page_id)
    if page is None:
        flash(
            "WikiPage not found!",
            "alert-warning",
        )
    else:
        flash(
            "WikiPage deleted successfully",
            "alert-success",
        )
        db.session.delete(page)
        db.session.commit()

    return redirect(url_for('wiki.home'))

@mod_wiki.route('/search', methods=['POST', 'POST'])
@mod_wiki.route('/search/', methods=['POST'])
@login_required
def search():
    """Search for a specific wiki with keyword"""
    form = SearchForm()
    if form.validate_on_submit():
        # Show the user the list of results (form.results maybe?)
        return render_template('wiki/search.html', form=form, results=form.results)
    else:
        flash_form_errors(form)
        return render_template('wiki/home.html', form=form)
