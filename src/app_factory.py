# app_factory.py

from flask import Flask

from db import db
from endpoint.landing.blueprint import landing_bp
from endpoint.image.blueprints import image_bp

def create_app(config_object):
    app = Flask(config_object.APP_NAME)
    app.config.from_object(config_object)
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    ## Landing Page
    app.register_blueprint(landing_bp)
    app.register_blueprint(image_bp)
    
    return app
