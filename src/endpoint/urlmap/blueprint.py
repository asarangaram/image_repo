from flask import Blueprint
from flask_restful import Api
from .resources import URLMapResource

URL_map_resouce_bp = Blueprint(
    'utils', __name__, url_prefix='/utils')
api = Api(URL_map_resouce_bp)

api.add_resource(URLMapResource, '/urlmap')
