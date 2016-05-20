from kotoba.kotoba import Kotoba

from imagination.entity        import *
from imagination.factorization import *
from imagination.exception     import *
from imagination.helper        import mixin

class AbstractRegistrar(mixin.ParameterParsingMixin):
    def __init__(self, transformer):
        self._transformer = transformer

    @property
    def locator(self):
        """
        The injected locator via the data transformer.

        :rtype: imagination.locator.Locator
        """
        return self._transformer.locator()

    def required_attributes(self):
        raise NotImplementedError('The attribute-name-to-description map must be defined.')

    @restrict_type(Kotoba)
    def validate(self, node):
        entity_type = node.name()

        required_attributes = self.required_attributes()

        for name in required_attributes:
            if node.attribute(name):
                continue

            raise IncompatibleBlockError(
                'Block "{}" needs the "{}" attribute being defined.'.format(
                    entity_type, required_attributes[name]
                )
            )

    def register(self, node):
        entity_id = node.attribute('id')

        params = self._get_params(node)
        entity = self.construct(node, params)

        raw_attr_interceptable = node.attribute('interceptable')

        entity.interceptable = self._transformer.cast(raw_attr_interceptable or 'false', 'bool')
        entity.tags          = self.__get_tags(node)

        self.locator.set(entity_id, entity)

    def construct(self, node, params):
        raise NotImplementedError('Required to implement')

    @restrict_type(Kotoba)
    def __get_tags(self, node):
        tags = node.attribute('tags')

        return tags and split(' ', tags.strip()) or []

class EntityRegistrar(AbstractRegistrar):
    def element_names(self):
        return ['entity']

    def required_attributes(self):
        return {
            'id':    'entity identifier',
            'class': 'entity class',
        }

    def construct(self, node, params):
        id     = node.attribute('id')
        kind   = node.attribute('class')
        loader = Loader(kind)

        return Entity(id, loader, *params.largs, **params.kwargs)

class FactorizationRegistrar(AbstractRegistrar):
    def element_names(self):
        return ['factorization']

    def required_attributes(self):
        return {
            'id':   'factorized entity identifier',
            'with': 'factory entity identifier',
            'call': 'factory method',
        }

    def construct(self, node, params):
        factory_id     = node.attribute('with')
        factory_method = node.attribute('call')

        return Factorization(self.locator, factory_id, factory_method, params)

class CallableRegistrar(AbstractRegistrar):
    def element_names(self):
        return ['callable']

    def required_attributes(self):
        return {
            'id':     'callable identifier',
            'method': 'callable method path (used by the "import" statement)',
            'static': 'the flag to cache the end result'
        }

    def construct(self, node, params):
        entity_type = node.name()
        method_path = node.attribute('method')

        is_static = self._transformer.cast(node.attribute('static') or 'true', 'bool')

        ProxyClass = OnceProxy if entity_type == 'definition' else CallbackProxy

        return ProxyClass(method_path, params.largs, params.kwargs, is_static)
