"""Forms for the wiki module

Author: Logan Gore
This file lists all forms to be filled out from within the wiki module.
"""

from flask_wtf import (
    Form,
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
        res = True
        if not Form.validate(self):
            res = False

        self.page = WikiPage(name=self.name.data, content=self.content.data)
        return res


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
