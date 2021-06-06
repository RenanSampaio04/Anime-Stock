from flask import Flask

from .animes_view import bp as bp_anime

def init_app(app: Flask):
    app.register_blueprint(bp_anime)
