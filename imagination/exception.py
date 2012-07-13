class MisplacedValidatorError(Exception):
    ''' Exception thrown when a validator is used with type (e.g., class, perimitive types etc.) '''

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
