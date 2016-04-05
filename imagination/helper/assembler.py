from re import split

from kotoba.kotoba import Kotoba
from kotoba        import load_from_file

from imagination.decorator.validator import restrict_type
from imagination.entity              import *
from imagination.factorization       import Factorization, NotReadyError
from imagination.exception           import *
from imagination.loader              import Loader
from imagination.helper.data         import *
from imagination.meta.aspect         import Contact
from imagination.meta.interception   import Interception
from imagination.meta.package        import Parameter
from imagination.proxy               import Proxy

from . import extension
from . import mixin

class Assembler(mixin.ParameterParsingMixin):
    """
    The entity assembler via configuration files.

    :param imagination.helper.data.Transformer transformer: the data transformer

    .. versionadded:: 1.5

        This class is added.

    .. versionchanged:: 1.9

        Added the support for entity factorization.

    .. versionchanged:: 1.10

        Added the support for delayed injections when the factory service is not ready to use during the factorization.

    .. versionchanged:: 1.20

        Supports callable proxies, execute-only-once proxies, and reference proxies.

    """
    __known_interceptable_events = ['before', 'pre', 'post', 'after']
    __entity_element_required_attributes = {
        'entity': {
            'id':    'entity identifier',
            'class': 'entity class',
        },
        'factorization': {
            'id':   'factorized entity identifier',
            'with': 'factory entity identifier',
            'call': 'factory method',
        },
        'callable': {
            'id':     'execution identifier',
            'method': 'callable method path (used by the "import" statement)',
            'cached': 'whether to cache the result'
        },
    }

    @restrict_type(Transformer)
    def __init__(self, transformer):
        self._transformer = transformer

        self.__interceptions = []
        self.__known_proxies = {}
        self.__delay_injection_map = {}

        self.__extensions = [
            extension.EntityRegistrar(self._transformer),
            extension.FactorizationRegistrar(self._transformer),
            extension.CallableRegistrar(self._transformer),
        ]

    def activate_passive_loading(self):
        """ Activate the passive loading mode.

            This is to delay the instantiation or forking of an entity to when
            it is referred/queried but undefined. This assumes that the queried
            entity will later be defined.

            If later on it isn't defined, the exception will be thrown.

            When this method is used, please do not forget to call :meth:`deactivate_passive_loading`
            to disable the passive mode.

            .. versionadded:: 1.7
        """
        self.locator.in_passive_mode = True

    def deactivate_passive_loading(self):
        """ Deactivate the passive loading mode.

            When :meth:`activate_passive_loading` is used, this method must be
            called to disable the passive mode.

            .. versionadded:: 1.7
        """

        if self.__delay_injection_map:
            injection_order = []

            for k in self.__delay_injection_map:
                di = self.__delay_injection_map[k]
                n  = di['node']
                p  = di['ping']
                r  = di['ready']

                if not n or r: # Skip if either the node is not defined or the delay injection is done for this entry.
                    continue

                di['ready'] = True

                injection_order.append((k, di['node'], di['ping']))

            injection_order.sort(key=lambda i: i[2])

            for di in injection_order:
                id, node, ping = di

                self.__get_interceptions(node)
                self.__register_entity(node)

            self.__activate_interceptions()

        self.locator.in_passive_mode = False

    def load(self, filepath):
        """
        Load the configuration.

        :param str filepath: the file path to the configuration.
        """
        xml = load_from_file(filepath)

        # First, register proxies to entities (for lazy initialization).
        for node in xml.children():
            self.__validate_node(node)
            self.__register_proxy(node)

        # Then, register loaders for entities.
        for node in xml.children():
            self.__get_interceptions(node)
            self.__register_entity(node)

        self.__activate_interceptions()

    def __activate_interceptions(self):
        # Then, declare interceptions to target entities.
        for interception in self.__interceptions:
            self.locator\
                .get_wrapper(interception.actor.id)\
                .register_interception(interception)

        self.__interceptions = []

    @property
    def locator(self):
        """
        The injected locator via the data transformer.

        :rtype: imagination.locator.Locator
        """
        return self._transformer.locator()

    @restrict_type(Kotoba)
    def __validate_node(self, node):
        """ .. deprecated:: 1.20 """
        entity_type = node.name()

        for ext in self.__extensions:
            if entity_type not in ext.element_names():
                continue

            ext.validate(node)

    @restrict_type(Kotoba)
    def __register_proxy(self, node):
        id    = node.attribute('id')
        proxy = Proxy(self.locator, id)

        self.locator.set(id, proxy)

        # this is for interceptors
        self.__known_proxies[id] = proxy

    @restrict_type(Kotoba)
    def __register_entity(self, node):
        entity_type = node.name()

        try:
            for ext in self.__extensions:
                if entity_type not in ext.element_names():
                    continue

                ext.register(node)

        except NotReadyError as e:
            required = str(e)
            targeted = node.attribute('id')

            self.__set_delay_injection(required, None, True)
            self.__set_delay_injection(targeted, node, False)

    def __set_delay_injection(self, id, node, ping):
        if id not in self.__delay_injection_map:
            self.__delay_injection_map[id] = {
                'ping':  0,
                'node':  node,
                'ready': False,
            }

        injection = self.__delay_injection_map[id]

        if node:
            injection['node'] = node

        if ping:
            injection['ping'] -= 1

    @restrict_type(Kotoba)
    def __get_interceptions(self, node):
        for sub_node in node.children('interception'):
            self.__interceptions.append(self.__get_interception(sub_node))

    @restrict_type(Kotoba)
    def __get_interception(self, node):
        actor = None
        event = None

        intercepted_action = None
        handling_action    = None

        for given_event in self.__known_interceptable_events:
            given_actor = node.attribute(given_event)

            # If the actor is not defined, continue or if the event is already
            # set (in the earlier iteration), raise the exception.
            if not given_actor:
                continue
            elif event:
                raise MultipleInterceptingEventsWarning(given_event)

            # Initially get the name of the actor and the handler.
            actor   = given_actor
            handler = node.parent().attribute('id')

            if actor == Interception.self_reference_keyword():
                actor = handler

            # If the actor or the handler has no proxies, raise the exception.
            if actor not in self.__known_proxies:
                raise UnknownProxyError('The target ({}) of the interception is unknown.'.format(actor))

            if handler not in self.__known_proxies:
                raise UnknownProxyError('The handler ({}) of the interception is unknown.'.format(handler))

            actor   = Contact(self.__known_proxies[actor], node.attribute('do'))
            handler = Contact(self.__known_proxies[handler], node.attribute('with'), self._get_params(node))
            event   = given_event

        return Interception(event, actor, handler)
