from flask import Blueprint
from flask_restful import Api

from .resources import Upload, Image, ImageDetails, Images

image_bp = Blueprint("image_bp", __name__, url_prefix="/image")

api = Api(image_bp)
api.add_resource(Upload, "/upload")
api.add_resource(Image, "/<int:image_id>")

api.add_resource(ImageDetails, "/<int:image_id>/details")
api.add_resource(Images, "/list")

