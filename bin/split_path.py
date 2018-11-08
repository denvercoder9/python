"""Pipe a string to split it at each colon

Indended mainly to be used with $PATH - you'd think there'd be an easier way
to do this...

"""

import sys
import itertools

print '\n'.join(itertools.chain.from_iterable(line.split(':')
                for line in sys.stdin.readlines()))
