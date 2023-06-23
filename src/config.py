# config.py
import os

class ConfigClass(object):
    APP_NAME = "Image Repo"
    try:
        SECRET_KEY = os.environ['FLASK_SECRET_KEY1'] 
    except: 
        SECRET_KEY = 'Secret!'
    PROPAGATE_EXCEPTIONS = True
    
    # Flask-SQLAlchemy
    password = os.environ['MYSQL_IMAGE_REPO_ADMIN_PW']
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://image_repo_admin:{password}@localhost/image_repo_db"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Save
    FILE_STORAGE_LOCATION = "/home/anandas/storage/image_repo"
    