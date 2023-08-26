from PIL import Image, ImageFile
import hashlib

# TODO: Do we need to record if the image is truncated?
ImageFile.LOAD_TRUNCATED_IMAGES = True


def sha512hash(image_data):
    with Image.open(image_data) as im:
        hash = hashlib.sha512(im.tobytes()).hexdigest()
    return hash
