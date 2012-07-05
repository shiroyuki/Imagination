from kotoba.kotoba import Kotoba

from imagination.decorator.validator import AllowedParameterType
from imagination.exception import *
from imagination.loader import Loader
from imagination.locator import Locator

#@AllowedParameterType(Locator)
class Transformer(object):
    '''
    Data transformer

    :param `locator`: the entity locator (as an instance of :class:`imagination.locator.Locator`)
    '''
    def __init__(self, locator):
        assert isinstance(locator, Locator), "Expecting an instance of imagination.locator.Locator, one of %s was given instead." % (type(locator).__name__)

        self.__locator = locator

    def cast(data, kind):
        '''
        Transform the given data to the given kind.

        :param `data`: the data to be transform
        :param `kind`: the kind of data of the transformed data
        :returns: the data of the given kind
        '''

        if kind == 'entity':
            data = self.__locator.get(data)
        elif kind == 'class':
            data = Loader(data).package()
        elif kind == 'int':
            data = int(data)
        elif kind == 'float':
            data = float(data)
        elif kind == 'bool':
            data = unicode(data).capitalize()

            assert data == 'True' or data == 'False'

            data = data == 'True'

        return data

class ParameterPackage(object):
    '''
    Parameter Package represents the parameter of arguments as
    a list and a dictionary to any callable objects (e.g.,
    constructor and methods).

    :param `largs`:  a list of arguments
    :param `kwargs`: a dictionary of arguments
    '''
    def __init__(self, largs=[], kwargs={}):
        try:
            assert isinstance(node, Kotoba), 'kotoba.kotoba.Kotoba'
        except AssertionError, e:
            raise ValueError, 'Expecting a node of %s' % e.message

        self.largs  = largs
        self.kwargs = kwargs

class TagPackage(list):
    def __init__(self, node):
        pass

class Entity(object):
    '''
    Meta data for Entity

    :param `node`:        an instance of :class:`kotoba.kotoba.Kotoba`
    '''

    def __init__(self, node):
        try:
            assert isinstance(node, Kotoba), 'Kotoba'
        except AssertionError, e:
            raise ValueError, 'Both parameters must be of types imagination.helper.meta.Transformer and kotoba.kotoba.Kotoba respectively. (Original message: %s)' % e.message

        try:
            assert node.attribute('id') and node.attribute('class'),\
                'The meta data of this entity does not have an identifier (ID) or class.'
        except AssertionError, e:
            raise IncompatibleBlockError, e.message

        self.id         = node.attribute('id')
        self.kind       = node.attribute('class')
        self.parameters = ParameterPackage(transformer, node)
        self.tags
