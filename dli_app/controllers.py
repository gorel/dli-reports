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

from dli_app import app

# Set all routing for the default app (not within modules)
@app.route('/')
@app.route('/home')
@app.route('/index.html')
def home():
    return 'Hello World!'
