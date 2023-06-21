# config.py
import os

class ConfigClass(object):
    APP_NAME = "Image Repo"
    try:
        SECRET_KEY = os.environ['FLASK_SECRET_KEY1'] 
    except: 
        SECRET_KEY = 'Secret!'
    PROPAGATE_EXCEPTIONS = True
    