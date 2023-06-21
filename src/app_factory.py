# app_factory.py

from flask import Flask
from endpoint.landing.blueprint import landing_bp

def create_app(config_object):
    app = Flask(config_object.APP_NAME)
    app.config.from_object(config_object)
    
    ## Landing Page
    app.register_blueprint(landing_bp)
    
    return app