#!/usr/bin/env python

"""Print the difference between two folders"""

import os

import click


def header(string):
    return "\n{}\n{}".format(string, '-'*len(string))


@click.command()
@click.argument('first_dir')
@click.argument('second_dir')
def main(first_dir, second_dir):
    first = set(os.listdir(first_dir))
    second = set(os.listdir(second_dir))

    print header("{}".format(first_dir))
    for file_ in first - second:
        print file_

    print header("{}".format(second_dir))
    for file_ in second - first:
        print file_

    print header("Both")
    for file_ in first & second:
        print file_


if __name__ == '__main__':
    main()
