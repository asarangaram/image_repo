from flask import Blueprint
from flask_restful import Api
from .resources import LandingPage

landing_bp = Blueprint('landing_bp', __name__, url_prefix='')
api = Api(landing_bp)

api.add_resource(LandingPage, '/')