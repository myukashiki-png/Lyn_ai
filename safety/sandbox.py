import os

SAFE_ROOT = os.path.abspath("workspace")

def safe_path(path):
    full = os.path.abspath(path)
    if not full.startswith(SAFE_ROOT):
        raise PermissionError("Akses ditolak.")
    return full
