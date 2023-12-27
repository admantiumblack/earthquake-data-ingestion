import sys
from pathlib import Path


def get_root_directory():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent.absolute()
    else:
        return Path(sys.modules["__main__"].__file__).parent.absolute()


def resolve_path(file_name):
    return get_root_directory() / file_name
