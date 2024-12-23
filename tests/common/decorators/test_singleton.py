import threading
from common.decorators import singleton, SingletonMeta


@singleton
class SingletonClass:
    """
    A test class to validate the singleton decorator.
    """

    def __init__(self, value):
        self.value = value


def test_singleton_single_thread():
    """
    Test that the singleton decorator ensures the same instance is returned in a single thread.
    """
    # Reset the singleton cache before the test
    SingletonMeta.reset_instances()

    obj1 = SingletonClass(42)
    obj2 = SingletonClass(99)

    assert obj1 is obj2  # Both should point to the same instance
    assert obj1.value == 42  # The value should remain as set by the first instance
    assert obj2.value == 42  # Any subsequent instance should have the same value


def test_singleton_multi_thread():
    """
    Test that the singleton decorator ensures the same instance is returned in a multithreaded environment.
    """
    # Reset the singleton cache before the test
    SingletonMeta.reset_instances()

    results = []

    def create_instance(value):
        instance = SingletonClass(value)
        results.append(instance)

    # Create threads that attempt to instantiate the SingletonClass
    threads = [threading.Thread(target=create_instance, args=(i,)) for i in range(5)]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # All threads should have received the same instance
    assert all(instance is results[0] for instance in results)
    assert results[0].value == 0  # Only the first value should be retained
