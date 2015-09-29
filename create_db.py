from dli_app import db

from dli_app.mod_account.models import *
from dli_app.mod_admin.models import *
from dli_app.mod_auth.models import *
from dli_app.mod_reports.models import *
from dli_app.mod_wiki.models import *

db.create_all()
