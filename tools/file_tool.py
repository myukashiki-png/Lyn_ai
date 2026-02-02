import os

ALLOWED_DIR = "workspace/"

def list_files():
    return os.listdir(ALLOWED_DIR)

