import os

def create_dir(dir_name):
    if not os.path.isdir(dir_name):
        try:
            os.makedirs(dir_name)
        except:
            pass