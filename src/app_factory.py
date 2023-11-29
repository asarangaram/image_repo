# app_factory.py
import os
from flask import Flask

from .db import db
from .endpoint.landing.blueprint import landing_bp
from .endpoint.image.blueprints import image_bp
from .endpoint.urlmap.blueprint import URL_map_resouce_bp
from . import lock

from .endpoint.urlmap.resources import URLMapResource


def create_app(config_object):

    if lock.instance_already_running(config_object):
        print("A instance is already accessing file storage")
        exit(-1)
    app = Flask(config_object.APP_NAME,
                template_folder=os.path.abspath('./src/html'))
    app.config.from_object(config_object)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    URLMapResource.init_app(app)

    # Landing Page
    app.register_blueprint(landing_bp)
    app.register_blueprint(image_bp)
    app.register_blueprint(URL_map_resouce_bp)

    return app
