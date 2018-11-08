"""
Small utility to replace ugly shell for-loops. For example, replace:

    for f in `ls -1`; do md5sum $f; done

...with this:

    ls -1 | map md5sum

This is still experimental and not battle tested!
"""

import sys
import subprocess


def main():
    cmd = sys.argv[1]
    for line in sys.stdin.readlines():
        subprocess.call([cmd, line.strip()])


if __name__ == '__main__':
    main()
