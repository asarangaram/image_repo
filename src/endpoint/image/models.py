import os
import shutil

from werkzeug.datastructures import FileStorage
from datetime import datetime

from db import db
from config import ConfigClass
from image_proc import hash
from image_proc.file_utilities import load_image_from_werkzeug_cache as image_loader

class ImageModelException(Exception):
    pass

class ImageModel(db.Model):
    __private_key = object()

    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.UnicodeText, nullable=False)
    path = db.Column(db.UnicodeText, nullable=True)
    datetime = db.Column(db.DateTime, nullable=False)
    exif_json = db.Column(db.JSON, default={})
    thumbnail = db.Column(db.LargeBinary, default=b"")
    hash_json = db.Column(db.JSON, default={})
    sha512hash = db.Column(db.String(128), nullable=False, unique=True)

    def __init__(self, image, sha512hash, private_key=None):
        if private_key != ImageModel.__private_key:
            raise ImageModelException("Use Class Method  receive_file.")
        self.name = image.filename
        self.datetime = datetime.now()
        self.sha512hash = sha512hash

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def set_path(self):
        self.path = os.path.join(
            ConfigClass.FILE_STORAGE_LOCATION, f"image_{str(self.id)}", self.name
        )
        self.save_to_db()

        return

    def save_image(self, bytes_io, overwrite=True):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "wb") as file:
            file.write(bytes_io.getvalue())
        self.save_to_db()
        return

    def jsonify(self):
        result = {
            "upload time": self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            
        }
        return result

    @classmethod
    def find_by_sha512hash(cls, sha512hash):
        return cls.query.filter_by(sha512hash=sha512hash).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        all = cls.query.all()
        return all

    @classmethod
    def create(cls, image: FileStorage):
        entity = None
        try:
            image_data = image_loader(image)
            sha512hash = hash.sha512hash(image_data=image_data)

            has_duplicate = cls.find_by_sha512hash(sha512hash)
            if has_duplicate:
                return has_duplicate, f"Duplicate Found"

            entity = ImageModel(
                image=image, sha512hash=sha512hash, private_key=cls.__private_key
            )

            if entity:
                entity.save_to_db()
                entity.set_path()
                entity.save_image(image_data)
                return entity, None
            raise ImageModelException("Failed to upload")
        except Exception as e:
            return entity, str(e)

    @classmethod
    def get(cls, _id):
        try:
            item = cls.find_by_id(_id)
            if item:
                return item, None
            raise ImageModelException("Item not found")

        except Exception as e:
            return None, str(e)
    @classmethod
    def get_all(cls):
        try:
            all = cls.find_all()
            if all:
                result = {}
                for image in all:
                    result[image.id] = image.jsonify()
                return result, None
            raise ImageModelException("No image found" )
        except Exception as e:
            return None, str(e)
    
    @classmethod
    def delete(cls, _id: int):
        try:
            item = cls.find_by_id(_id)

            if item:
                print(f"PATH IS {item.path}")
                shutil.rmtree(os.path.dirname(item.path))
                item.delete_from_db()
                return None
            raise ImageModelException("Item is not found; Not deleted")
        except Exception as e:
            return str(e)
