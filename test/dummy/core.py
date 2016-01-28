class ObjectWithListAndDict(object):
    def __init__(self, l=[], d={}, t=tuple()):
        self.l = l
        self.d = d
        self.t = t

class PlainOldObject(object):
    def __init__(self):
        self.name = 'something'

    def method(self):
        return 0

class PlainOldObjectWithParameters(object):
    def __init__(self, a, b, do_multiply=True):
        self.a = a
        self.b = b
        self.d = do_multiply

    def method(self):
        r = self.d and self.a * self.b or self.a / self.b

        return r

class DependencyInjectableObjectWithClass(object):
    def __init__(self, reference):
        self.r = reference
        self.i = reference()

class DependencyInjectableObjectWithEntity(object):
    def __init__(self, entity):
        self.e = entity
