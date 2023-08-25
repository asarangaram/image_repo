import json
import os
import shutil
import base64
from dateutil import parser
from ...db import db
from ...image_proc.metadata import ExifTool
import humanize


class ImageModelException(Exception):
    pass


class EXIFModel(db.Model):
    __private_key = object()

    __tablename__ = "exif_data"

    id = db.Column(db.Integer, primary_key=True)

    image_id = db.Column(db.Integer, db.ForeignKey('images.id'))

    FileSize = db.Column(db.Integer)
    MIMEType = db.Column(db.Text)
    Model = db.Column(db.Text)
    Make = db.Column(db.Text)

    YResolution = db.Column(db.Integer)
    XResolution = db.Column(db.Integer)
    ResolutionUnit = db.Column(db.Integer)
    Orientation = db.Column(db.Integer)
    ImageSize = db.Column(db.Text)

    ExifImageHeight = db.Column(db.Integer)
    ExifImageWidth = db.Column(db.Integer)
    ImageWidth = db.Column(db.Integer)
    ImageHeight = db.Column(db.Integer)

    FileModifyDate = db.Column(db.Text)
    FileAccessDate = db.Column(db.Text)
    CreateDate = db.Column(db.Text)
    ModifyDate = db.Column(db.Text)
    DateTimeOriginal = db.Column(db.Text)

    GPSAltitudeRef = db.Column(db.Integer)
    GPSLatitudeRef = db.Column(db.Text)
    GPSProcessingMethod = db.Column(db.Text)
    GPSLongitudeRef = db.Column(db.Text)
    GPSTimeStamp = db.Column(db.Text)
    GPSDateStamp = db.Column(db.Text)
    GPSDateTime = db.Column(db.Text)
    GPSPosition = db.Column(db.Text)
    GPSAltitude = db.Column(db.Double)
    GPSLatitude = db.Column(db.Double)
    GPSLongitude = db.Column(db.Double)

    yy = db.Column(db.Integer)
    mm = db.Column(db.Integer)
    dd = db.Column(db.Integer)
    HH = db.Column(db.Integer)
    DAY = db.Column(db.Integer)

    def __init__(self, data, private_key=None):
        if private_key != EXIFModel.__private_key:
            raise ImageModelException("Use Class Method  fromJSON.")

        for key, value in data.items():
            setattr(self, key, value)

        if self.DateTimeOriginal:
            temp0 = self.DateTimeOriginal
            dateTime = temp0.split(' ')
            temp1 = f"{dateTime[0].replace(':', '-')} {dateTime[1]}"
            print(f"{temp0} -> {temp1}")
            temp = parser.parse(temp1)
            self.yy = temp.year
            self.mm = temp.month
            self.dd = temp.day
            self.HH = temp.hour
            self.DAY = temp.weekday()

    def __repr__(self):
        attributes = ', '.join([f"{key}={value}" for key, value in self.__dict__.items()])
        return f"EXIFModel({attributes})"

    @classmethod
    def fromJSON(cls, json_data):
        exif = EXIFModel(json_data, private_key=cls.__private_key)
        return exif

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        all = cls.query.all()
        return all

    @classmethod
    def read_from_image(cls, image):
        metadata = ExifTool.exiftool(image.path)
        exif = EXIFModel.fromJSON(metadata)
        exif.image_id = image.id

        exif.save_to_db()

        return exif
