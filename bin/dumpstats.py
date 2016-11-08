#!/usr/bin/env python

"This dumps a stat file that the python profiler creates"

import sys
import pstats


if __name__ == '__main__':
    filename = sys.argv[1]
    s = pstats.Stats(filename)
    s.sort_stats('time').print_stats(10)
