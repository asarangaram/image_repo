
import os
import json

import cv2
from sqlalchemy import Column, Integer, JSON, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
"""
It is intentional that create_all() is not called
"""


class FaceDB(Base):

    __tablename__ = 'faces'

    create_table_query = """
        CREATE TABLE IF NOT EXISTS faces (
            id INT AUTO_INCREMENT PRIMARY KEY,
            json_data JSON
        )
    """
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

    @classmethod
    def create_table(cls, session):
        session.execute(text(cls.create_table_query))
