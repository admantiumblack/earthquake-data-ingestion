import sys
from pathlib import Path

def get_root_directory():

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    else:
        return Path(sys.modules['__main__'].__file__)

def resolve_path(file_name):
    return get_root_directory() / file_name