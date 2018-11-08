from itertools import chain
import os
from os.path import expanduser, abspath, join


def all_files(folder):
    """Return complete paths for all files under `folder` """
    return chain(join(d, f) for d, _, files in os.walk('.') for f in files)


def system_path(path):
    """Automatically expand user and return absolute path"""
    return abspath(expanduser(path))
