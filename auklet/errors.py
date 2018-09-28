class AukletException(Exception):
    pass


class AukletConnectionError(AukletException):
    pass


class AukletConfigurationError(AukletException):
    """
    Raise for invalid credentials passed to
    Monitoring class upon instantiation
    """
    pass
