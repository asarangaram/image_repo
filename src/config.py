# config.py
import os


def get_required_env_variable(var_name):
    value = os.environ.get(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' is not set.")
    return value


class ConfigClass(object):
    APP_NAME = get_required_env_variable('APP_NAME')
    try:
        SECRET_KEY = get_required_env_variable('FLASK_SECRET_KEY1')
    except BaseException:
        SECRET_KEY = 'Secret!'
    PROPAGATE_EXCEPTIONS = True

    # Flask-SQLAlchemy
    repo = get_required_env_variable('MYSQL_IMAGE_REPO')
    user = get_required_env_variable('MYSQL_IMAGE_REPO_ADMIN')
    password = get_required_env_variable('MYSQL_IMAGE_REPO_ADMIN_PW')

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@localhost/{repo}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File Save
    FILE_STORAGE_LOCATION = get_required_env_variable('FILE_STORAGE_LOCATION')
