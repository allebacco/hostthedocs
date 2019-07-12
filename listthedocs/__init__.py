import os

from flask import Flask

from .client import ListTheDocs


__version__ = '1.0.0'


def create_app(override_config: dict=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, 'listmydocs.sqlite'),
        MAX_CONTENT_LENGTH=8 * 1024 * 1024,
    )

    app.config.from_pyfile('config.py', silent=True)
    if override_config is not None:
        app.config.update(override_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    print(app.instance_path)

    # Initialize database
    from . import database
    database.init_app(app)

    # Setup endpoints
    from . import projects, webui
    app.register_blueprint(projects.projects_apis)
    app.register_blueprint(webui.webui)

    return app


def serve():
    from .service import app, getconfig

    getconfig.serve(app)
