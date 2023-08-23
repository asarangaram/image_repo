from flask import request, send_file
from flask_restful import Resource
import logging

from .models import ImageModel


class RepoException(Exception):
    pass


class Upload(Resource):
    def post(cls):
        logging.debug("post called")
        try:
            if "image" not in request.files:
                logging.debug("No image provided")
                raise RepoException("No image provided")
            image = request.files["image"]
            if image.filename == "":
                logging.debug("No image name provided")
                raise RepoException("No image name provided")
            object, err = ImageModel.create(image=image)
            result = {}
            if object:
                result = object.jsonify()
                result["id"] = object.id
            if err:
                result["message"] = err
                return result, 500

            return result, 201
        except Exception as e:
            logging.debug(str(e))
            return {"message": str(e)}, 400


class Image(Resource):
    def get(cls, image_id: int):
        try:
            image, e = ImageModel.get(image_id)
            if e:
                return {"message": e}, 400

            return send_file(
                image.path, mimetype="image/jpeg", download_name=image.name
            )

        except Exception as e:
            return {"message": e}, 400

    def delete(cls, image_id: int):
        e = ImageModel.delete(image_id)
        if e:
            return {"message": e}, 400
        return {"success": "Image deleted successfully"}


class Images(Resource):
    def get(cls):
        all, e = ImageModel.get_all()
        if e:
            return {"message": e}, 400
        return {"images": all}, 201

    def delete(cls):
        all, e = ImageModel.delete_all()
        if e:
            return {"message": e}, 400
        return {"images": all}, 201


class ImageMetadata(Resource):
    def get(cls, image_id: int):
        metadata, e = ImageModel.get_metadata_by_id(image_id)
        if e:
            return {"message": e}, 400

        return metadata, 201


class ImageThumbnail(Resource):
    def get(cls, image_id: int):
        try:
            image, e = ImageModel.get(image_id)
            if e:
                return {"message": e}, 400
            thumbnail, e = image.get_thumbnail_path()
            if e:
                return {"message": e}, 400
            return send_file(
                thumbnail, mimetype="image/jpeg", download_name=f"{image_id}_thumbnail.png"
            )

        except Exception as e:
            return {"message": e}, 400
