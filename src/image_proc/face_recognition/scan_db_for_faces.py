import os
import sys
import cv2
import json
import time
from loguru import logger

from src.config import ConfigClass

from src.image_proc.face_recognition.db_access.image import ImageDB, DBase
from src.image_proc.face_recognition.db_access.faces import FaceDB
from src.image_proc.face_recognition.detect_face_facenet_pytorch import detect_faces

logger.remove(0)
logger.add("performance.log", format="{time} | {level} | {message}", level="INFO")
logger.add(sys.stdout, format="{time} | {level} | {message}", level="INFO")


class FaceScanner(FaceDB):
    def detect_faces(self, method: str, detect_faces_fn):
        if method not in self.json:
            img = cv2.imread(self.json["path"])
            faces = detect_faces_fn(img, prob_low=0.9)
            self.json[method] = faces
            self.save_faces(
                faces, method, img, os.path.dirname(self.json["path"]))

    def save_faces(self, faces, method, img, path):
        for i, face in enumerate(faces):
            x0, y0, x1, y1 = face["pos"]

            face_cropped = img[y0:y1, x0:x1]
            # Generate a filename for the cropped face
            output_path = os.path.join(path, f'face_{str(i).zfill(4)}.png')
            output_path = output_path.replace("image_repo", f"image_repo_{method}")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            # Save the cropped face
            cv2.imwrite(output_path, face_cropped)
        pass


def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        logger.info(f"Execution time: {execution_time:.2f} ms")
        return result
    return wrapper


@measure_time
def detect_all(start=0, count=1000):
    images = ImageDB(ConfigClass.SQLALCHEMY_DATABASE_URI).get_images(limit=10, offset=0)

    with DBase(ConfigClass.SQLALCHEMY_DATABASE_URI) as db:
        FaceScanner.create_table(db.session)
        for image in images:
            faceDB = FaceScanner(image)
            faceDB.detect_faces("facenet_pytorch", detect_faces)
            faceDB.save(db.session)


if __name__ == '__main__':
    for i in range(200):
        detect_all(start=i * 100, count=100)
