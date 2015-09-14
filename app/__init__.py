# System imports
import sys

# Flask imports
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

# Define the web app
sys.stdout.write('Creating Flask app...')
app = Flask(__name__)
sys.stdout.write('Done\n')

# Configurations for the app
sys.stdout.write('Loading config from object...')
app.config.from_object('config')
sys.stdout.write('Done\n')

# Define the database
sys.stdout.write('Defining SQLAlchemy database...')
db = SQLAlchemy(app)
sys.stdout.write('Done\n')

# Register error handlers
sys.stdout.write('Registering error handlers...')
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
sys.stdout.write('Done\n')

# Import all blueprints from controllers
from app.mod_account.controllers import mod_account
from app.mod_admin.controllers import mod_admin
from app.mod_auth.controllers import mod_auth
from app.mod_reports.controllers import mod_reports
from app.mod_wiki.controllers import mod_wiki

# Register bluesys.stdout.writes
sys.stdout.write('Registering bluesys.stdout.write modules...')
app.register_blueprint(mod_account)
app.register_blueprint(mod_admin)
app.register_blueprint(mod_auth)
app.register_blueprint(mod_reports)
app.register_blueprint(mod_wiki)
sys.stdout.write('Done\n')

# Build database with SQLAlchemy
sys.stdout.write('Building database with SQLAlchemy...')
db.create_all()
sys.stdout.write('Done\n')

sys.stdout.write('\nApp done loading.\n')
