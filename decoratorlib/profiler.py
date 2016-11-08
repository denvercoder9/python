import cProfile


def profile(f):
    """Useful decorator for profiling a function"""

    def wrapper(*args, **kwargs):
        p = cProfile.Profile()
        res = p.runcall(f, *args, **kwargs)
        print p.print_stats()
        return res
    return wrapper
