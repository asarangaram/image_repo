
import os
import json

import cv2
from sqlalchemy import Column, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FaceDB(Base):
    __tablename__ = 'faces'
    id = Column(Integer, primary_key=True)
    json_data = Column(JSON)

    def __init__(self, image):

        self.id = image["id"]
        self.json = image

    def save(self, session):
        self.json_data = json.dumps(self.json)
        r = self.load(session, self.id)
        if r:
            r.json_data = self.json_data
        else:
            session.add(self)

        session.commit()

    @classmethod
    def load(cls, session, user_id):
        return session.query(cls).get(user_id)
