def debug(func):
    """Print the function signature and return value"""
    def wrapper(*args, **kwargs):
        print(f"Calling '{func.__name__}' with args: {args} kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"'{func.__name__}' returned: {result}")
        return result
    return wrapper
