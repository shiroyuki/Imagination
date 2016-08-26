# v2
class Wrapper(object):
    """ Relay Container

        This is to allow interceptions on an object without modifying the
        object attributes or instance methods.

        :param callable core_get: a callable reference to the associated :method:`Imagination.get`.
        :param object instance: a wrapped instance
        :param dict interceptions: the event-type-to-method-name-to-interception map
    """
    def __init__(self, core_get, instance, interceptions):
        self.__dict__ = {
            '_internal_core_get'        : core_get,
            '_internal_instance'        : instance,
            '_internal_interceptions'   : interceptions,
            '_internal_cache_callables' : {},
        }

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        cached_callables = self.__dict__['_internal_cache_callables']

        if name in cached_callables:
            return cached_callables[name]

        interceptions = self.__dict__['_internal_interceptions']

        core_get = self.__dict__['_internal_core_get']
        instance = self.__dict__['_internal_instance']

        if not hasattr(instance, name):
            raise AttributeError('{} has no attribute "{}".'.format(type(actual_object).__name__), name)

        returning_callable = getattr(instance, name)

        if name in interceptions:
            interceptable_callable = InterceptableCallable(
                core_get,
                returning_callable,
                interceptions[name]
            )

            cached_callables[name] = interceptable_callable

            return interceptable_callable

        return returning_callable

class InterceptableCallable(object):
    """ Interceptable callable object """
    def __init__(self, core_get, callable_reference, interceptions):
        self._internal_core_get      = core_get
        self._internal_callable      = callable_reference
        self._internal_interceptions = interceptions

    def _has_interceptions(self, event_type):
        return bool(self._internal_interceptions[event_type])

    def _intercept(self, event_type, largs = None, kwargs = None, error = None, returning = False):
        if not self._has_interceptions(event_type):
            return

        largs  = largs  or []
        kwargs = kwargs or {}

        for interception in self._internal_interceptions[event_type]:
            interceptor         = self._internal_core_get(interception.interceptor_id)
            intercepting_method = getattr(interceptor,
                                          interception.intercepting_method)

            if error:
                intercepting_method(error, *largs, **kwargs)
            else:
                intercepting_method(*largs, **kwargs)

    def __call__(self, *largs, **kwargs):
        self._intercept('before', largs, kwargs, returning = False)

        result = None

        if self._has_interceptions('error'):
            try:
                result = self._internal_callable(*largs, **kwargs)
            except Exception as e:
                self._intercept('error', largs, kwargs, error, returning = False)

                return
        else:
            result = self._internal_callable(*largs, **kwargs)

        if self._has_interceptions('after'):
            return self._intercept('after', [result], returning = True)

        return result
