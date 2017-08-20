# v2
def is_wrapper(obj):
    return hasattr(obj, '__imagination_wrapper__')


class Wrapper(object):
    """ Relay Container

        This is to allow interceptions on an object without modifying the object attributes or instance methods.

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

    # This is just a special property to identify as __class__ is overridden to fakely representing the wrapped object.
    # NOTE apparently, isinstance accepts both the actual class (Wrapper) and the hack method.
    __imagination_wrapper__ = True

    @property
    def __class__(self):
        return type(self.__dict__['_internal_instance'])

    @classmethod
    def __subclasshook__(cls, C):
        return cls in (self.__type__, type(self.__dict__['_internal_instance']))

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
            raise AttributeError('{} has no attribute "{}".'.format(type(instance).__name__, name))

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
    """ Interceptable callable object

        This class is to actually handle the call operation with the ability to intercept the activity.
    """
    def __init__(self, core_get, callable_reference, interceptions):
        self._internal_core_get      = core_get
        self._internal_callable      = callable_reference
        self._internal_interceptions = interceptions

    def _has_interceptions(self, event_type):
        return bool(self._internal_interceptions[event_type])

    def _intercept(self, event_type, largs = None, kwargs = None, error = None):
        if not self._has_interceptions(event_type):
            return

        largs  = largs  or []
        kwargs = kwargs or {}

        last_result = None

        for interception in self._internal_interceptions[event_type]:
            interceptor         = self._internal_core_get(interception.interceptor_id)
            intercepting_method = getattr(interceptor,
                                          interception.intercepting_method)

            try:
                if error:
                    intercepting_method(error, *largs, **kwargs)

                    continue

                intercepting_method(*largs, **kwargs)
            except TypeError:
                raise InterceptionError('Unable to execute the method "{}" from {} ({}.{}) with args = {} and kwargs = {}'.format(
                    intercepting_method.__name__,
                    interception.interceptor_id,
                    type(interceptor).__module__,
                    type(interceptor).__name__,
                    largs,
                    kwargs,
                ))

    def __call__(self, *largs, **kwargs):
        self._intercept('before', largs, kwargs)

        result = None

        if self._has_interceptions('error'):
            try:
                result = self._internal_callable(*largs, **kwargs)
            except Exception as error:
                self._intercept('error', largs, kwargs, error)

                raise error
        else:
            result = self._internal_callable(*largs, **kwargs)

        if self._has_interceptions('after'):
            self._intercept('after', [result])

        return result


class InterceptionError(TypeError):
    """ Unable to intercept the method call """
