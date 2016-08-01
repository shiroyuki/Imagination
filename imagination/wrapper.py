# v2
class Wrapper(object):
    """ Relay Container

        This is to allow interceptions on an object without modifying the
        object attributes or instance methods.
    """
    def __init__(self, core_get, instance, interceptions):
        self.__dict__ = {
            '_internal_core_get'      : core_get,
            '_internal_instance'      : instance,
            '_internal_interceptions' : interceptions,
        }

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        core_get = self.__dict__['_internal_core_get']
        instance = self.__dict__['_internal_instance']

        interceptions = self.__dict__['_internal_interceptions']

        if not hasattr(instance, name):
            raise AttributeError('{} has no attribute "{}".'.format(type(actual_object).__name__), name)

        return getattr(instance, name)
