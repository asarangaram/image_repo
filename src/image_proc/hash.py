from PIL import Image
import hashlib

def sha512hash(image_data):   
    with Image.open(image_data) as im:
        hash = hashlib.sha512(im.tobytes()).hexdigest()
    return hash
    