class DeprecatedAPI(Exception):
    ''' Exception thrown when a deprecated API is used. '''

class MisplacedValidatorError(Exception):
    ''' Exception thrown when a validator is used with type (e.g., class, perimitive types etc.) '''

class ForbiddenForkError(Exception):
    ''' Exception thrown only when a locator try to fork a proxy. '''

class DuplicateKeyWarning(Warning):
    ''' Warning thrown when an internal dictionary detects an attempt of re-assignment to the direction by the existed key. '''

class MultipleInterceptingEventsWarning(Warning):
    ''' Warning thrown when more than one intercepting event is detected. '''

class IncompatibleBlockError(Exception):
    ''' Exception thrown when :meth:`imagination.locator.Locator.load_xml` cannot process the entity block. '''

class UnknownFileError(Exception):
    ''' Exception thrown when :meth:`imagination.locator.Locator.load_xml` cannot locate the file on the given path. '''

class UnknownEntityError(Exception):
    ''' Exception thrown when :class:`imagination.locator.Locator` constructor receives an unusable entity. '''

class UnknownProxyError(Exception):
    ''' Exception thrown when :class:`imagination.helper.assembler.Assembler` could not find the proxy. '''

class NonCallableError(Exception):
    ''' Exception thrown when :class:`imagination.action.Action` tries to execute a non-callable reference. '''

class LockedEntityException(Exception):
    '''
    Exception thrown when a caller attempts to update any of alterable properties
    of an instance of :class:`imagination.entity.Entity` when it is in the locked
    state.
    '''

class InstantiationError(RuntimeError):
    """ Exception thrown when forking fails. """
