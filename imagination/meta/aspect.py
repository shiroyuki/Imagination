from imagination.meta.package import Parameter
from imagination.proxy        import Proxy

class Contact(object):
    def __init__(self, proxy, method_name, parameters=None):
        self._proxy       = proxy
        self._method_name = method_name
        self._parameters  = parameters

    @property
    def id(self):
        return self._proxy.id

    @property
    def method_name(self):
        return self._method_name

    @property
    def interface(self):
        return self._proxy.load().__getattribute__(self._method_name)

    @property
    def parameters(self):
        return self._parameters

    def engage(self):
        return self.interface(*self._parameters.largs, **self._parameters.kwargs)