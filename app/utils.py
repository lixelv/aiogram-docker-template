from functools import wraps
from time import time


def timer(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time()
        result = await func(*args, **kwargs)
        end = time()
        print(f"Function {func.__name__} took {(end - start) * 1000:.2f} ms")
        return result

    return wrapper
