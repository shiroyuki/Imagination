class SpecialType(object):
    function = 'function' # function representative

def allowed_type(*allowed_list, **allowed_dictionary):
    def inner_decorator(reference):
        return StrictTypedCallableObject(reference, *allowed_list, **allowed_dictionary)

    return inner_decorator

class StrictTypedCallableObject(object):
    def __init__(self, function, *allowed_list, **allowed_dictionary):
        self.function     = function
        self.allowed_list = allowed_list
        self.allowed_dictionary = allowed_dictionary

    def __call__(self, *largs, **kwargs):
        allowed_list = self.allowed_list[:len(largs)]

        for index in range(len(allowed_list)):
            if not allowed_list[index]:
                continue

            kind = allowed_list[index]

            assert isinstance(largs[index], kind), kind.__name__

        for key, kind in self.allowed_dictionary.iteritems():
            if key not in kwargs:
                continue

            assert isinstance(kwargs[key], kind), kind.__name__
        return self.function(*largs, **kwargs)