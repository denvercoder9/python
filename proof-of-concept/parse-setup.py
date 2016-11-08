"""
Parses a setup.py file and downloads the dependencies from pypi.

Not very useful, but it was fun to play with the AST...

"""

import ast
import os.path
import tempfile
from distutils.version import LooseVersion

import requests


def parse_dependencies(code):
    """
    Because even importing setup.py executes it, read the file as
    text, tranform it into an abstract syntax tree (AST) and iterate
    over it until the "install_requires" keyword argument has been found:
    these are our dependencies.
    """
    syntax_tree = ast.parse(code)
    for stmt in syntax_tree.body:
        if isinstance(stmt, ast.Expr) and stmt.value.func.id == 'setup':
            break

    for kw in stmt.value.keywords:
        if kw.arg == 'install_requires':
            for value in kw.value.elts:
                yield value.s


def parse_version(dependency):
    """
    Parse versions to decide which one to download

    None means latest available.

    == gets exactly that version
    <= gets exactly that version
    >, >= and no specified version all defaults to latest.
    <  tries to subtract one from the most minor part of the version tuple
    """
    if '==' in dependency:
        return dependency.split('==')
    elif '<=' in dependency:
        return dependency.split('<=')
    elif '>=' in dependency:
        return dependency.split('>=')[0], None
    elif '>' in dependency:
        return dependency.split('>')[0], None
    elif '<' in dependency:
        name, versions = dependency.split('<')
        parts = map(int, versions.split('.'))
        new_version = '.'.join(map(str, parts[:-1] + [parts[-1]-1]))
        return name, new_version
    else:
        return dependency, None


def get_filename_and_url(name, version):
    """
    Always query pypi about correct versions, filenames and
    URLs. pypi-URLs are case sensitive and might fail if we
    try to build them ourselves...
    """
    url = 'https://pypi.python.org/pypi/{}/json'.format(name)
    metadata = requests.get(url)
    metadata.raise_for_status()
    releases = metadata.json()['releases']
    if not version:
        version = sorted(releases.keys(), key=LooseVersion)[-1]

    for meta in releases[version]:
        if meta['packagetype'] == 'sdist':
            return meta['filename'], meta['url']


def fetch_from_pypi(url):
    """ Fetch file from URL and return its contents """
    download = requests.get(url)
    download.raise_for_status()
    return download.content


def main():
    print 'Parsing setup.py...'
    dependencies = parse_dependencies(open('setup.py').read())

    temp_dir = tempfile.gettempdir()
    print 'Temporary directory is {}'.format(temp_dir)

    for dependency in dependencies:
        try:
            name, version = parse_version(dependency)
            filename, url = get_filename_and_url(name, version)

            print 'Downloading {}...'.format(filename)
            content = fetch_from_pypi(url)
            path = os.path.join(temp_dir, filename)
            with open(path, 'w+') as f:
                f.write(content)
        except Exception as e:
            print "\n{}\n".format(e)


if __name__ == '__main__':
    main()
