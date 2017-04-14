# v2
class UndefinedContainerIDError(RuntimeError):
    """ Error when an undefined container ID is requested. """


class MissingParameterException(ValueError):
    """ Exception when a parameter is missing """


class UnexpectedParameterException(ValueError):
    """ Exception when the unexpected parameter is defined """


class UndefinedDefaultValueException(ValueError):
    """ Exception when the default value is not defined """


class UnexpectedDefinitionTypeException(ValueError):
    """ Exception when the type of the definition is not the same as the annotated type. """


class DuplicateKeyError(Exception):
    """ Error thrown when an internal dictionary detects an attempt of re-assignment to the direction by the existed key. """


class UnknownEnvironmentVariableError(Exception):
    """ Unknown environment variable error """
