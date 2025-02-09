import logfire
from functools import wraps


def log_function_result(func, args, kwargs, result):
    line = f"Function {func.__name__} returned {result.__class__.__name__}"
    logfire.debug(line, args=args, kwargs=kwargs, result=result)


def logfire_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        log_function_result(func, args, kwargs, result)

        return result

    return wrapper


def async_logfire_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        log_function_result(func, args, kwargs, result)

        return result

    return wrapper


def decorate_methods(decorator):
    def result_decorator(cls):
        for method_name, method in cls.__dict__.items():
            if callable(method) and not method_name.startswith("_"):
                setattr(cls, method_name, decorator(method))
        return cls

    return result_decorator


def logfire_class_decorator(cls):
    return decorate_methods(logfire_decorator)(cls)


def async_logfire_class_decorator(cls):
    return decorate_methods(async_logfire_decorator)(cls)
