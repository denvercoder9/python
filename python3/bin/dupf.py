#!/usr/bin/env python3

"""DUPlicate Finder"""

from collections import defaultdict
from hashlib import md5
from pathlib import Path
import os
import sys


def next_path(root):
    for dir_, _, files in os.walk(root):
        for fil in files:
            yield Path(dir_, fil).absolute()


def get_hash(path):
    try:
        return md5(path.read_bytes()).hexdigest()
    except OSError:
        print(f'{path} could not be read.')


def find_duplicates(root):
    fs = defaultdict(list)

    for path in next_path(root):
        key = get_hash(path)
        fs[key].append(path)

    for key, paths in fs.items():
        if len(paths) > 1:
            yield key, paths


def main():
    folders = sys.argv[1:]
    if not len(folders):
        sys.exit('Please provide at least one folder.')

    for folder in folders:
        for key, paths in find_duplicates(folder):
            print(f'{key}')
            for path in paths:
                print(f'   {path}')


if __name__ == '__main__':
    main()
