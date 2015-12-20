#!/usr/bin/env python

"""
Small script to locate duplicates within a filesystem.

Uses md5-hash to identify files. Is thus subject to the same (very rare)
collision problems as any other md5 based application. This is also the
reason why the final removal of the duplicate files is left to the
administrator himself.
"""

import os
from hashlib import md5
from collections import defaultdict

import click


def all_paths(root_dir):
    """Generate all absolute paths under the root directory"""
    for dir_, _, files in os.walk(root_dir):
        for file_ in files:
            yield os.path.join(dir_, file_)


def get_file_hash(path):
    """Returns the md5 hash of a file"""
    with open(path, 'r') as f:
        contents = f.read()
        return md5(contents).hexdigest()


def create_hash_dict(root_dir):
    """Returns a dictionary with md5 hash as key, and absolute paths of the
    files having this hash as values"""
    hash_dict = defaultdict(list)

    for path in all_paths(root_dir):
        file_hash = get_file_hash(path)
        hash_dict[file_hash].append(path)
    return hash_dict


@click.command()
@click.argument('root_dir')
def main(root_dir):
    hash_dict = create_hash_dict(root_dir)

    for contents_hash, paths in hash_dict.items():
        if len(paths) > 1:
            print contents_hash
            for path in paths:
                print '\t{}'.format(path)
            print


if __name__ == "__main__":
    main()
