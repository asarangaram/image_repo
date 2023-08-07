
from tendo import singleton

def instance_already_running(config_object):
    lock_file = f"{config_object.FILE_STORAGE_LOCATION}/app.lock"
    try:
        singleton.SingleInstance(lockfile=lock_file) 
        already_running = False
    except IOError:
        already_running = True

    return already_running