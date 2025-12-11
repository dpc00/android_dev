import pstats
from cProfile import Profile
from functools import wraps

profiler = Profile()


def profile(
    cumulative=True,
    print_stats=10,
    sort_stats="cumulative",
    dump_stats=False,
    profile_filename="profilestats.out",
):
    def closure(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            result = None
            if cumulative:
                global profiler
            else:
                profiler = Profile()
            profiler.enable()
            try:
                func(*args, **kwargs)
            finally:
                profiler.disable()
                if dump_stats:
                    profiler.dump_stats(profile_filename)
                stats = pstats.Stats(profiler)
                # conv = pyprof2calltree.CalltreeConverter(stats)
                # with open(callgrind_filename, 'w') as fd:
                #     conv.output(fd)
                if print_stats:
                    stats.strip_dirs().sort_stats(sort_stats).print_stats(print_stats)
            return result

        return decorator

    return closure
