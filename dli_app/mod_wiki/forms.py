"""Forms for the wiki module

Author: Logan Gore
This file lists all forms to be filled out from within the wiki module.
"""

from flask_wtf import (
    Form,
)

from sqlalchemy import (
    or_,
)

from wtforms import (
    TextAreaField,
    TextField,
    validators,
)

from dli_app.mod_wiki.models import (
    WikiPage,
)


class EditWikiPageForm(Form):
    """A form for editing WikiPages"""

    def __init__(self, *args, **kwargs):
        """Initialize the EditWikiPage form"""
        Form.__init__(self, *args, **kwargs)
        self.page = None

    def validate(self):
        """Validate the form"""
        if not Form.validate(self):
            return False

        self.page = WikiPage(name=self.name.data, content=self.content.data)
        return True


    name = TextField(
        "Page name",
        validators=[
            validators.Required(
                message="Please give this Wiki Page a name.",
            ),
        ],
    )

    content = TextAreaField(
        "Content",
        validators=[
            validators.Required(
                message="Please enter the content for this Wiki Page",
            ),
        ],
    )


class SearchForm(Form):
    """A form for searching WikiPages"""

    def __init__(self, *args, **kwargs):
        """Initialize the SearchForm form"""
        Form.__init__(self, *args, **kwargs)
        self.results = []

    def validate(self):
        """Validate the form"""
	res = True
        if not Form.validate(self):
	    res = False

	query = '%{}%'.format(self.search_box.data)
	self.results = WikiPage.query.filter(or_(
	    WikiPage.name.like(query),
	    WikiPage.content.like(query)
	)).all()

        return res


    search_box = TextField(
        "Wiki Search",
        validators=[
            validators.Required(
                message="You must enter at least one keyword.",
            ),
        ],
    )
