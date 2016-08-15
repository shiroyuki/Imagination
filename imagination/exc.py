# v2
class UndefinedContainerIDError(RuntimeError):
    """ Error when an undefined container ID is requested. """


class UnexpectedParameterException(ValueError):
    """ Exception when the unexpected parameter is defined """


class UndefinedDefaultValueException(ValueError):
    """ Exception when the default value is not defined """
