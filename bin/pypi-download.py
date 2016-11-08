#!/usr/bin/env python

"""Small script to grab files from pypi.

Depending on distribution format, this might or might not work. 

Just for fun. You should most certainly use pip instead.

"""

import click
import requests


@click.command()
@click.argument('name')
@click.argument('version')
def pypi_download(name, version):
    filename = '{name}-{version}.tar.gz'.format(name=name, version=version)
    url = 'https://pypi.python.org/packages/source/{name[0]}/{name}/{filename}'.format(
        name=name, version=version, filename=filename)

    r = requests.get(url)
    with open(filename, 'w+') as f:
        f.write(r.content)


pypi_download()
