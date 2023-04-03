import os

def check_path_exists(path):
    try:
        os.stat(path)
    except:
        return False
    return True
