import sys
import unittest

if sys.version_info >= (3, 3):
    from imagination.core import Imagination
    from imagination.exc  import UnexpectedDefinitionTypeException
    from imagination.meta.container import Entity
    from imagination.meta.definition import DataDefinition, ParameterCollection


class FunctionalTest(unittest.TestCase):
    """ Test the support for positional and key-value arguments/parameters """
    def setUp(self):
        if sys.version_info < (3, 3):
            self.skipTest('The tested feature is not supported in Python {}.'.format(sys.version))

    def test_ok_1(self):
        core = Imagination()

        fixed_param_a      = DataDefinition(123, 'a', 'int', False)
        positional_param_1 = DataDefinition('bangkok', None, 'str', False)
        keyword_param_1    = DataDefinition('bangkok', 'foo', 'str', False)

        params = ParameterCollection()
        params.add(fixed_param_a, 'a')
        params.add(positional_param_1)
        params.add(keyword_param_1, 'foo')

        entity = Entity('dp', 'dummy.dynamic_param.DynamicParamObject', params)

        core.set_metadata('dp', entity)

        core.get('dp')

    def test_ok_2(self):
        core = Imagination()

        fixed_param_a      = DataDefinition(123, 'a', 'int', False)
        positional_param_1 = DataDefinition('bangkok', None, 'str', False) # this replaces fixed param b
        keyword_param_1    = DataDefinition('chiang mai', 'north', 'str', False)
        keyword_param_2    = DataDefinition('songkla', 'south', 'str', False)

        params = ParameterCollection()
        params.add(fixed_param_a)
        params.add(positional_param_1)
        params.add(keyword_param_1)
        params.add(keyword_param_2)

        entity = Entity('dp', 'dummy.dynamic_param.FancyDynamicParamObject', params)

        core.set_metadata('dp', entity)

        core.get('dp')

    def test_ok_3(self):
        core = Imagination()

        positional_param_1 = DataDefinition('bangkok', None, 'str', False) # this replaces fixed+optional param a
        keyword_param_1    = DataDefinition('chiang mai', 'north', 'str', False)
        keyword_param_2    = DataDefinition('songkla', 'south', 'str', False)

        params = ParameterCollection()
        params.add(positional_param_1)
        params.add(keyword_param_1)
        params.add(keyword_param_2)

        entity = Entity('dp', 'dummy.dynamic_param.SuperDynamicParamObject', params)

        core.set_metadata('dp', entity)

        core.get('dp')

    def test_unexpected_definition_type(self):
        core = Imagination()

        fixed_param_a = DataDefinition('bangkok', 'a', 'str', False)
        positional_param_1 = DataDefinition('bangkok', None, 'str', False)

        params = ParameterCollection()
        params.add(fixed_param_a, 'a')
        params.add(positional_param_1)

        entity = Entity('dp', 'dummy.dynamic_param.DynamicParamObject', params)

        core.set_metadata('dp', entity)

        self.assertRaises(UnexpectedDefinitionTypeException, core.get, 'dp')
