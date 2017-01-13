class DynamicParamObject(object):
    def __init__(self, a : int, *b, **c):
        self.a = a
        self.b = b
        self.c = c

class SuperDynamicParamObject(object):
    def __init__(self, x = None, *a, **b):
        self.x = x
        self.a = a
        self.b = b

class FancyDynamicParamObject(object):
    def __init__(self, a : int, b, *c, **d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
