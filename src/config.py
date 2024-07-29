# config.py
import os


def get_required_env_variable(var_name):
    value = os.environ.get(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' is not set.")
    return value

def check_path(path):
    parent_dir = os.path.dirname(path)
    return  os.path.exists(parent_dir)
        
    

class ConfigClass(object):
    APP_NAME = get_required_env_variable('APP_NAME')
    try:
        SECRET_KEY = get_required_env_variable('FLASK_SECRET_KEY1')
    except BaseException:
        SECRET_KEY = 'Secret!'
    PROPAGATE_EXCEPTIONS = True

    # Flask-SQLAlchemy
    repo = get_required_env_variable('IMAGE_REPO_DB')
    user = get_required_env_variable('IMAGE_REPO_DB_ADMIN')
    password = get_required_env_variable('IMAGE_REPO_DB_ADMIN_PW')
    try:
        use_mysql = get_required_env_variable('USE_MYSQL')
    except BaseException:
        use_mysql = False 

    if use_mysql:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@localhost/{repo}"
    elif check_path(repo):
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{repo}"
    else :
        print('Invalid db path')
        

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File Save
    FILE_STORAGE_LOCATION = get_required_env_variable('FILE_STORAGE_LOCATION')
