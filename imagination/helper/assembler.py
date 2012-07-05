from kotoba.kotoba import Kotoba

from imagination.helper.meta import *

class Assembler(object):
    '''
    :param `transformer`: an instance of :class:`imagination.helper.meta.Transformer`
    '''
    def __init__(self, transformer):
        try:
            assert isinstance(transformer, Transformer), 'imagination.helper.meta.Transformer'
        except AssertionError, e:
            raise ValueError, 'Expected an instance of %s' % e.message

        self.transformer = transformer

    def get_entity(self, node):
        '''
        :param `node`: an instance of :class:`kotoba.kotoba.Kotoba`
        '''
        try:
            assert isinstance(node, Kotoba), 'kotoba.kotoba.Kotoba'
        except AssertionError, e:
            raise ValueError, 'Expected an instance of %s' % e.message


    def get_param(self, node):
        '''
        :param `node`: an instance of :class:`kotoba.kotoba.Kotoba`
        '''
        try:
            assert isinstance(node, Kotoba), 'kotoba.kotoba.Kotoba'
        except AssertionError, e:
            raise ValueError, 'Expected an instance of %s' % e.message

        package = ParameterPackage(node)

        index = 0

        for param in node.children('param'):
            try:
                assert not param.attribute('name')\
                    or not param.attribute('type'),\
                    'The parameter #%d does not have either name or type.' % index
            except AssertionError, e:
                raise IncompatibleBlockError, e.message

            index += 1
            name   = param.attribute('name')

            if package.kwargs.has_key(name):
                raise DuplicateKeyWarning, 'There is a paramenter with that name already registered.'

            package.kwargs[name] = transformer.cast(
                param.data(),
                param.attribute('type')
            )

        return package