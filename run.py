from dli_app import app

app.config.from_object('config')
app.run(
    host=app.config['SERVER_HOST'],
    port=app.config['SERVER_PORT'],
    debug=app.config['DEBUG'],
    threaded=True,
)
