import sys
import os
import logging
import pytest
import unittest
import json
from glob import glob

sys.path.append('..')
from src.wsgi import app

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
mylogger = logging.getLogger()

class MyTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home(self):
        try:
            output = self.app.get('/')
            received_json = json.loads(output.data)
            mylogger.info(received_json)
            if not received_json["hello"] == "guest":
                assert False
        except:
            assert(False)
        assert(True)

    def image_upload(self, image_name, image):
        
        data = {
            'image': (open(image, 'rb'), image_name)
        }
        output = self.app.post('/image/upload', data=data)
        received_json = json.loads(output.data)
        mylogger.info(received_json)
        assert ("id" in received_json)
            
    def test_image_upload_single_image(self):
        test_image = "/disks/data/onedrive/mediaFromAnandaS/grouped/windows_phone/ExtraMedia/Photos/Photos/WP_20150722_12_09_29_Pro.jpg"
        self.image_upload("WP_20150722_12_09_29_Pro2.jpg", test_image)
    
    def test_image_upload_dir_recursive(self):
        source_dir = "/disks/data/onedrive/mediaFromAnandaS/grouped/windows_phone/ExtraMedia"
        images = [y for x in os.walk(source_dir) for y in glob(os.path.join(x[0], '*.*'))]

        for image in images:
            image_name = os.path.basename(image)
            self.image_upload(image_name=image_name, image=image)
            
if __name__ == '__main__':
    
    mylogger.info(' About to start the tests ')
    pytest.main(args=[os.path.abspath(__file__)])
    mylogger.info(' Done executing the tests ')
        