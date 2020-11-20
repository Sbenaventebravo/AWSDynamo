from singleton import SingletonMeta


def test_singleton_pattern_works():
    """Testing if the singleton pattern only generates a unique object"""
    class Client(metaclass=SingletonMeta):
        pass

    first_client = Client()
    second_client = Client()

    assert first_client is second_client


def test_singleton_pattern_not_applyied():
    """Testing if the without singleton two object are not equals"""
    class Client():
        pass

    first_client = Client()
    second_client = Client()

    assert first_client is not second_client
