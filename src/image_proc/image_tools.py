from PIL import Image


class ImageToolsException(Exception):
    pass


class ImageTools(object):

    def __init__(self, filename):
        self.image_name = filename

    def __enter__(self):
        self.original_image = Image.open(self.image_name)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def create_thumbnail(self):

        try:
            print("Creating thumbnail for image {self.image_name}")

            thumbnail_size = (100, 100)  # Todo: Configurable
            thumbnail_image = self.original_image.copy()
            thumbnail_image.thumbnail(thumbnail_size)

            thumbnail_image_bytes = thumbnail_image.convert("RGB").tobytes()
            return thumbnail_image_bytes
        except Exception as e:
            raise ImageToolsException(f"Failed to create thumbnail; {e}")
