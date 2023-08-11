from io import BytesIO
from PIL import Image


class ImageToolsException(Exception):
    pass


class ImageTools(object):

    def __init__(self, filename):
        self.image_name = filename

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def create_thumbnail(self):
        print(f"Creating thumbnail for image {self.image_name}")
        try:
            image = Image.open(self.image_name)
            image.thumbnail((256, 256 - 64))
            # image.save(f"{self.image_name}.png", format='png')
            temp = BytesIO()
            image.save(temp, format='png')
            # thumbnail_image_bytes = image.convert("RGB").tobytes()

            return temp.getbuffer()
        except Exception as e:
            raise ImageToolsException(f"Failed to create thumbnail; {e}")
