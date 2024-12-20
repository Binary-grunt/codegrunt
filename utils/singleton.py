import threading
from functools import wraps
from typing import Type, TypeVar, Callable, Dict, Any

T = TypeVar('T')


def singleton(cls: Type[T]) -> Callable[..., T]:
    """
    A thread-safe decorator to turn a class into a Singleton.

    Args:
        cls (Type[T]): The class to be decorated as Singleton.

    Returns:
        Callable[..., T]: A wrapper function that returns the Singleton instance.
    """
    instances: Dict[Type[T], T] = {}
    lock = threading.Lock()

    @wraps(cls)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        with lock:
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper
