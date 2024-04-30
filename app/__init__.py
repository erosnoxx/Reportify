from flask import Flask
from dynaconf import FlaskDynaconf


def create_app() -> Flask:

    app = Flask(__name__)
    FlaskDynaconf(app, extensions_list=True)

    return app
