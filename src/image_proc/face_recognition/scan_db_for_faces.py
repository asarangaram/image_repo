import os
from src.config import ConfigClass

from src.image_proc.face_recognition.db_access.image import ImageDB, DBase
from src.image_proc.face_recognition.db_access.faces import FaceDB
from mtcnn.mtcnn import MTCNN
import cv2

# Create an MTCNN detector
detector = MTCNN()


def detect_faces(img):
    faces = detector.detect_faces(img)
    return [result['box'] for result in faces]


class FaceScanner(FaceDB):
    def detect_faces(self, method: str, detect_faces_fn):
        if method not in self.json:
            img = cv2.imread(self.json["path"])
            faces = detect_faces_fn(img)
            print(f'There are {len(faces)} faces in  {self.id}')
            self.json[method] = faces
            self.save_faces(faces, method, img, os.path.dirname(self.json["path"]))

    def save_faces(self, faces, method, img, path):
        for i, face in enumerate(faces):
            x, y, w, h = face
            face = img[y:y + h, x:x + w]
            # Generate a filename for the cropped face
            output_path = os.path.join(path, method, f'face_{str(i).zfill(4)}.png')
            output_path = output_path.replace("image_repo", "image_repo_faces")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            # Save the cropped face
            cv2.imwrite(output_path, face)
        pass


if __name__ == '__main__':
    images = ImageDB(ConfigClass.SQLALCHEMY_DATABASE_URI).get_images()

    with DBase(ConfigClass.SQLALCHEMY_DATABASE_URI) as db:
        for image in images:
            faceDB = FaceScanner(image)
            faceDB.detect_faces("mtcnn", detect_faces)
            faceDB.save(db.session)
