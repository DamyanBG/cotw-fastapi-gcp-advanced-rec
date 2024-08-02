import cProfile
import pstats
from functools import wraps


def profile_function(func):
    async def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = await func(*args, **kwargs)
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats("cumtime")
        stats.print_stats()
        return result

    return wrapper
